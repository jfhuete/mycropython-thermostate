from machine import Pin
import ntptime

from time import sleep

from logger import Logger
from net import Net

from sensors.temperature import Temperature


class Thermostate():

    # Pins In
    PIN_TEMP_SENSOR = Pin(4, Pin.IN)

    # Pins Out
    PIN_ENABLE_BOILER = Pin(2, Pin.OUT)

    def __init__(self, loop_delay=1):

        self.loop_delay = loop_delay

        self.state = {
            "dateSetted": False,
            "temp": None
        }

        # Modules
        self.net = Net()
        self.logger = Logger("LOOP")

        # Sensors
        self.temp_sensor = Temperature(self.PIN_TEMP_SENSOR)

    def connect_wifi(self):
        self.net.connect()

    def set_time(self):

        if self.state["dateSetted"]:
            return

        if self.net.connected:
            try:
                self.logger.info("Setting local date")
                ntptime.settime()
                self.state["dateSetted"] = True
                self.logger.info("Date setted")
            except OSError:
                self.logger.error(
                    "Can't to set local time. Network is not connected")
        else:
            self.logger.error(
                "Can't to set local time. Network is not connected")

    def read_temp_humidity(self):
        self.state.update(self.temp_sensor.measure())

    def works(self):
        self.connect_wifi()
        self.set_time()

        self.read_temp_humidity()

        self.PIN_ENABLE_BOILER.value(1)
        sleep(2)
        self.PIN_ENABLE_BOILER.value(0)

    def start(self):
        try:
            while True:
                self.works()
                sleep(self.loop_delay)
        except KeyboardInterrupt:
            self.net.disconnect()
