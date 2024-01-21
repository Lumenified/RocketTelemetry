class Payload:
    def __init__(self, data):
        self.description = data['description']
        self.weight = data['weight']

class Telemetry:
    def __init__(self, data):
        self.host = data['host']
        self.port = data['port']

class Timestamps:
    def __init__(self, data):
        self.launched = data['launched']
        self.deployed = data['deployed']
        self.failed = data['failed']
        self.cancelled = data['cancelled']

class Rocket:
    def __init__(self, data):
        self.id = data['id']
        self.model = data['model']
        self.status = data['status']
        self.mass = data['mass']
        self.payload = Payload(data['payload'])
        self.telemetry = Telemetry(data['telemetry'])
        self.timestamps = Timestamps(data['timestamps'])
        self.altitude = data['altitude']
        self.speed = data['speed']
        self.acceleration = data['acceleration']
        self.thrust = data['thrust']
        self.temperature = data['temperature']

    def get_data(self):
        return {
            'id': self.id,
            'model': self.model,
            'status': self.status,
            'mass': self.mass,
            'payload': vars(self.payload),
            'telemetry': vars(self.telemetry),
            'timestamps': vars(self.timestamps),
            'altitude': self.altitude,
            'speed': self.speed,
            'acceleration': self.acceleration,
            'thrust': self.thrust,
            'temperature': self.temperature
        }