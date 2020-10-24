import dht
from machine import Pin

from logger import Logger


class Temperature:

    PIN_TEMP_SENSOR = Pin(4, Pin.IN)

    def __init__(self, state):
        self.state = state
        self.sensor = dht.DHT22(self.PIN_TEMP_SENSOR)
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
