import dht
import machine

from logger import Logger

class Temperature:

    def __init__(self, pin=4):
        self.sensor = dht.DHT22(machine.Pin(pin))
        self.logger = Logger("TEMP")

    def measure(self):
        self.sensor.measure()

        temp = self.sensor.temperature()
        humidity = self.sensor.humidity()

        self.logger.info("Temp: {} ºC, Humid: {}".format(temp, humidity))

        return {
            "temp": temp,
            "humidity": humidity
        }
