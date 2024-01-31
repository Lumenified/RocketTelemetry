import socket
from flask_socketio import SocketIO
from flask import Response, Flask, request, jsonify, stream_with_context
import time
from receiveData import receive_data
from requestTry import make_request_with_retry
import atexit
import threading
import requests
from flask_cors import CORS
from RocketModel import Rocket
from WeatherModel import Weather
import json

#######################################################################################
#######################################################################################
#######################################################################################
#                                Global Variables                                     #
#######################################################################################
#######################################################################################
#######################################################################################
# Create the Flask app
app = Flask(__name__)
# Enable CORS
CORS(app, origins='http://localhost:3000')

# Create the SocketIO instance
socketio = SocketIO(app, cors_allowed_origins="*")

# List of ports to connect to
ports = [4000, 4001, 4002, 4003, 4004, 4005, 4006, 4007, 4008]

# List to store the sockets
sockets = []
# Thread value to fetch data
should_continue = False
# Thread counter
thread_counter = 0
# Number of connected devices
connected_device = 0
# List to store the data from rest api
data_list = [{} for _ in range(9)]
# Data from rest api
data_from_api = None
# Weather data from rest api
weather = None
# API endpoint
api_endpoint = 'http://localhost:5000/'

# Global headers
global_headers = {'x-api-key': 'API_KEY_1'}


#######################################################################################
#######################################################################################
#######################################################################################
#                                Helper Functions                                     #
#######################################################################################
#######################################################################################
#######################################################################################
# Connect to the port and return the socket
def connect_to_port(port):
    sock = None
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("127.0.0.1", port))
    except socket.error as e: # Catch the socket error
        print(f"Socket error: {e}")
    except socket.herror as e: # Catch 
        print(f"Address-related error: {e}")
    except socket.gaierror as e: # Catch getaddrinfo error
        print(f"Address-related error during getaddrinfo or getnameinfo: {e}")
    except socket.timeout as e:
        print(f"Timeout error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return sock

# Close all the sockets in the list
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

# Fetch data from each socket and emit it to the client    
def fetch_data(sockets):
    '''
    Fetch data from each socket and emit it to the client
    
    Parameters:
        sockets (list): The list of sockets to fetch data from
    
    Returns:
        None
    '''
def fetch_data(sockets):
    global should_continue
    previous_values = {}  # Store the last correct data for each rocket
    while should_continue:
        try:
            rocket_data = []
            for i, sock in enumerate(sockets):
                if sock.fileno() != -1:  # Check if the socket is still open
                    value = receive_data(sock)
                    if value['id'] not in previous_values or not is_significantly_different(previous_values[value['id']], value):
                        previous_values[value['id']] = value
                    if value['id'] in previous_values:
                        rocket_data.append(previous_values[value['id']])
            socketio.emit('update_data', rocket_data)
        except Exception as e:
            pass
        time.sleep(0.1)

def is_significantly_different(previous_value, current_value):
    # Define a threshold for each field
    thresholds = {
        'temperature': 1
    }
    for field in thresholds:
        if abs(previous_value[field] - current_value[field]) > thresholds[field]:
            return True
    return False

# Connect to each port and store the socket
def check_sockets():
    global sockets
    print(connected_device)

    if not should_continue:
        for port in ports:
            sock = connect_to_port(port)
            sockets.append(sock)


def fetch_weather_data():
    updated_weather = None
    while True:
        try:
            updated_weather = make_request_with_retry(f'{api_endpoint}/weather', global_headers)
        except Exception as e:
            pass
        time.sleep(5)
        return updated_weather

#######################################################################################
#######################################################################################
#######################################################################################
#                                           SSE                                       #
#######################################################################################
#######################################################################################
#######################################################################################
# Send the data to the client
def sse_format(data):
    return f"data: {json.dumps(data)}\n\n"

@app.route('/weather')
def weather():
    def generate():
        while True:
            time.sleep(5)
            data = fetch_weather_data()
            yield sse_format(data)

    return Response(stream_with_context(generate()), mimetype='text/event-stream')
#######################################################################################
#######################################################################################
#######################################################################################
#                                SocketIO Functions                                   #
#######################################################################################
#######################################################################################
#######################################################################################

# Connect to each port and store the socket
# Start the Flask-SocketIO server
@socketio.on('connect')
def handle_connect():
    global should_continue, sockets, thread_counter, connected_device
    connected_device += 1
    if connected_device == 1 and thread_counter == 0:
        check_sockets()
        should_continue = True
        thread = threading.Thread(target=fetch_data, args=(sockets,))
        thread_counter += 1
        thread.start()
    #print(connected_device)
    #print('Client connected')

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
    #print(connected_device)
    #print(sockets)
    print('Client disconnected')

#######################################################################################
#######################################################################################
#######################################################################################
#                                Flask Views                                          #
#######################################################################################
#######################################################################################
#######################################################################################
# Start the data fetching function in a separate view
    
    ##
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

# launch rocket
@app.route('/launch_rocket/<rocket_id>', methods=['GET'])
def launch_rocket(rocket_id):
    global global_headers
    try:
        rocket_url = f'{api_endpoint}/rocket/{rocket_id}/status/launched'
        headers = global_headers.copy()
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        response = make_request_with_retry(rocket_url, headers=headers, method='PUT', id=rocket_id, single=True)
        #print(response)
        rocket = Rocket(response)

        return jsonify(rocket.get_data()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# deploy rocket
@app.route('/deploy_rocket/<rocket_id>', methods=['GET'])
def deploy_rocket(rocket_id):
    global global_headers
    try:
        rocket_url = f'{api_endpoint}/rocket/{rocket_id}/status/deployed'
        response = make_request_with_retry(rocket_url, headers=global_headers, method='PUT', id=rocket_id, single=True)
        rocket = Rocket(response)
        #print(response)
        return jsonify(rocket.get_data()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# cancel rocket
@app.route('/cancel_rocket/<rocket_id>', methods=['GET'])
def cancel_rocket(rocket_id):
    global global_headers
    try:
        rocket_url = f'{api_endpoint}/rocket/{rocket_id}/status/launched'
        response = make_request_with_retry(rocket_url, headers=global_headers, method='DELETE', id=rocket_id, single=True)
        #print(response)
        rocket = Rocket(response)
        return jsonify(rocket.get_data()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


#######################################################################################
#######################################################################################
#######################################################################################
#                                Main                                                 #
#######################################################################################
#######################################################################################
#######################################################################################
# Start the Flask app
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8080, debug=True)

# Close the sockets when the program exits
atexit.register(close_sockets, sockets)