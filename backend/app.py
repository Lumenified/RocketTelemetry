import socket
from flask_socketio import SocketIO
from flask import render_template, Flask, redirect, url_for, request, jsonify
import time
from receiveData import receive_data
from requestTry import make_request_with_retry
import atexit
import threading
import requests
from flask_cors import CORS
from RocketModel import Rocket
from WeatherModel import Weather

############################################################################################################
            # Global variables
############################################################################################################
# Create the Flask app
app = Flask(__name__)
CORS(app, origins='http://localhost:3000')

# Create the SocketIO instance
socketio = SocketIO(app, cors_allowed_origins="*")

# List of ports to connect to
ports = [4000, 4001, 4002, 4003, 4004, 4005, 4006, 4007, 4008]

# List to store the sockets
sockets = []
# Thread value to fetch data
should_continue = False
thread_counter = 0
connected_device = 0
# List to store the data from rest api
data_list = [{} for _ in range(9)]
data_from_api = None
weather = None
# API endpoint
api_endpoint = 'http://localhost:5000/'

# Global headers
global_headers = {'x-api-key': 'API_KEY_1'}

############################################################################################################
            # Helper functions
############################################################################################################
def connect_to_port(port):
    sock = None
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("127.0.0.1", port))
    except socket.error as e:
        print(f"Socket error: {e}")
    except socket.herror as e:
        print(f"Address-related error: {e}")
    except socket.gaierror as e:
        print(f"Address-related error during getaddrinfo or getnameinfo: {e}")
    except socket.timeout as e:
        print(f"Timeout error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return sock

def close_sockets(sockets):
    '''
    Close all the sockets in the list
    
    Parameters:
        sockets (list): The list of sockets to close
        
    Returns:
        None
    '''
    for sock in sockets:
        try:
            sock.shutdown(socket.SHUT_RDWR)
            sock.close()
        except socket.error as e:
            print(f"Socket error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        
def fetch_data(sockets):
    '''
    Fetch data from each socket and emit it to the client
    
    Parameters:
        sockets (list): The list of sockets to fetch data from
    
    Returns:
        None
    '''
    global should_continue
    while should_continue:
        try:
            rocket_data = []
            #print(len(sockets))
            for i, sock in enumerate(sockets):
                if sock.fileno() != -1:  # Check if the socket is still open
                    value = receive_data(sock)
                    rocket_data.append(value)
            socketio.emit('update_data', rocket_data)
        except Exception as e:
            pass
        time.sleep(0.1)
        if not should_continue:
            break


def check_sockets():
    global sockets
    print(connected_device)

    if not should_continue:
        for port in ports:
            sock = connect_to_port(port)
            sockets.append(sock)


def update_weather():
    while should_continue:
        try:
            global weather
            start_time = time.time()
            weather = make_request_with_retry(f'{api_endpoint}/weather', global_headers)
            end_time = time.time()
            weather_instance = Weather(weather)
            socketio.emit('update_weather', weather_instance.get_data())
        except Exception as e:
            pass
        elapsed_time = end_time - start_time
        print(elapsed_time)
        time.sleep(10-elapsed_time)
        if not should_continue:
            break



############################################################################################################
            # Rocket SocketIO event handlers
############################################################################################################
# Start the Flask-SocketIO server
@socketio.on('connect')
def handle_connect():
    global should_continue, sockets, thread_counter, connected_device
    connected_device += 1
    if connected_device == 1 and thread_counter == 0:
        check_sockets()
        should_continue = True
        thread_rocket_data = threading.Thread(target=fetch_data, args=(sockets,))
        update_weather_thread = threading.Thread(target=update_weather)
        thread_counter += 2
        thread_rocket_data.start()
        update_weather_thread.start()
    print(connected_device)
    print('Client connected')

# Close the sockets when the client disconnects
@socketio.on('disconnect')
def handle_disconnect():
    global connected_device
    connected_device -= 1
    if connected_device == 0:
        global should_continue, sockets, thread_counter
        close_sockets(sockets)
        should_continue = False
        thread_counter = 0
        sockets = []
    print(connected_device)
    #print(sockets)
    print('Client disconnected')


############################################################################################################
            # Weather SocketIO event handlers
############################################################################################################

def update_weather():
    while should_continue:
        try:
            global weather
            weather = make_request_with_retry(f'{api_endpoint}/weather', global_headers)
            weather_instance = Weather(weather)
            socketio.emit('update_weather', weather_instance.get_data())
        except Exception as e:
            pass
        time.sleep(0.1)

############################################################################################################
            # Flask routes
############################################################################################################
# Start the data fetching function in a separate thread
@app.route('/', methods=['GET'])
def index():
    try:
        if request.method == 'GET':
            global data_from_api
            global weather
            data_from_api = make_request_with_retry(f'{api_endpoint}/rockets', global_headers)
            weather = make_request_with_retry(f'{api_endpoint}/weather', global_headers)
            rockets = [Rocket(data) for data in data_from_api]
            weather_instance = Weather(weather)
            return jsonify({'rockets': [rocket.get_data() for rocket in rockets], 'weather': weather_instance.get_data()})
        else:
            return jsonify({'error': 'Invalid request method'}), 400
    except requests.RequestException as e:
        return jsonify({'error': 'Failed to fetch data'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/launch_rocket/<rocket_id>', methods=['GET'])
def launch_rocket(rocket_id):
    global global_headers
    try:
        rocket_url = f'{api_endpoint}/rocket/{rocket_id}/status/launched'
        headers = global_headers.copy()
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        response = make_request_with_retry(rocket_url, headers=headers, method='PUT', id=rocket_id, single=True)
        print(response)
        rocket = Rocket(response)

        return jsonify(rocket.get_data()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/deploy_rocket/<rocket_id>', methods=['GET'])
def deploy_rocket(rocket_id):
    global global_headers
    try:
        rocket_url = f'{api_endpoint}/rocket/{rocket_id}/status/deployed'
        response = make_request_with_retry(rocket_url, headers=global_headers, method='PUT', id=rocket_id, single=True)
        rocket = Rocket(response)
        print(response)
        return jsonify(rocket.get_data()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/cancel_rocket/<rocket_id>', methods=['GET'])
def cancel_rocket(rocket_id):
    global global_headers
    try:
        rocket_url = f'{api_endpoint}/rocket/{rocket_id}/status/launched'
        response = make_request_with_retry(rocket_url, headers=global_headers, method='DELETE', id=rocket_id, single=True)
        print(response)
        rocket = Rocket(response)
        return jsonify(rocket.get_data()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


############################################################################################################
            # Main function
############################################################################################################
# Start the Flask app
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8080, debug=True)

# Close the sockets when the program exits
atexit.register(close_sockets, sockets)