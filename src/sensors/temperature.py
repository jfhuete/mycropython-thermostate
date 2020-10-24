import dht
from logger import Logger
from config.pins import PIN_TEMP_SENSOR


class Temperature:

    def __init__(self, state):
        self.state = state
        self.sensor = dht.DHT22(PIN_TEMP_SENSOR)
        self.logger = Logger(self.state, "TEMP")

    def measure(self):
        try:
            self.sensor.measure()

            temp = self.sensor.temperature()
            humidity = self.sensor.humidity()
            self.logger.info("Temp: {} ºC, Humid: {}%".format(temp, humidity))
        except OSError as e:
            temp = None
            humidity = None
            self.logger.error("Can't to read temperature {}".format(e))

        self.state.temperature_measured = temp
        self.state.humidity_measured = humidity
