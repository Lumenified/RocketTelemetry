class Precipitation:
    def __init__(self, data):
        self.probability = data['probability']
        self.rain = data['rain']
        self.snow = data['snow']
        self.sleet = data['sleet']
        self.hail = data['hail']

class Wind:
    def __init__(self, data):
        self.direction = data['direction']
        self.angle = data['angle']
        self.speed = data['speed']

class Weather:
    def __init__(self, data):
        self.temperature = data['temperature']
        self.humidity = data['humidity']
        self.pressure = data['pressure']
        self.precipitation = Precipitation(data['precipitation'])
        self.time = data['time']
        self.wind = Wind(data['wind'])

    def get_data(self):
        return {
            'temperature': self.temperature,
            'humidity': self.humidity,
            'pressure': self.pressure,
            'precipitation': vars(self.precipitation),
            'time': self.time,
            'wind': vars(self.wind)
        }