from machine import Pin
import ntptime

from time import sleep

from logger import Logger
from net import Net


class Thermostate():

    def __init__(self, loop_delay=1):

        self.loop_delay = loop_delay

        # Modules

        self.net = Net()
        self.logger = Logger()

        # Pins

        self.led = Pin(2, Pin.OUT)

    def connect_wifi(self):
        self.net.connect()

    def set_time(self):
        if self.net.connected:
            self.logger.info("Setting local date")
            ntptime.settime()
        else:
            self.logger.error(
                "Can't to set local time. Network is not connected")

    def works(self):
        self.connect_wifi()
        self.set_time()

        self.led.value(1)
        sleep(2)
        self.led.value(0)

    def start(self):
        while True:
            self.works()
            sleep(self.loop_delay)
