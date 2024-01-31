import math
import struct

# Create a function to receive data from the socket
def receive_data(sock, active=True):
    '''
    Receive data from the socket and return a dictionary of the data
    
    Parameters:
        sock (socket): The socket to receive data from
    
    Returns:
        dict: A dictionary of the data
    '''
    
    altitude = float('NaN')
    speed = float('NaN')
    acceleration = float('NaN')
    thrust = float('NaN')
    temperature = float('NaN')
    id = ''
    data = {}
    socket_data = sock.recv(36)
    try:
        id = struct.unpack('>10s', socket_data[1:11])[0].decode('utf-8')
        altitude = struct.unpack('>f', socket_data[13:17])[0]
        speed = struct.unpack('>f', socket_data[17:21])[0]
        acceleration = struct.unpack('>f', socket_data[21:25])[0]
        thrust = struct.unpack('>f', socket_data[25:29])[0]
        temperature = struct.unpack('>f', socket_data[29:33])[0]
    except:
        pass
    data['id'] = id
    data['altitude'] = 'NaN' if math.isnan(altitude) else altitude
    data['speed'] = 'NaN' if math.isnan(speed) else speed
    data['acceleration'] = 'NaN' if math.isnan(acceleration) else acceleration
    data['thrust'] = 'NaN' if math.isnan(thrust) else thrust
    data['temperature'] = 'NaN' if math.isnan(temperature) else temperature
    return data