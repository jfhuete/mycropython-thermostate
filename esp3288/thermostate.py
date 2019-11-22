from machine import Pin
from time import sleep


class Thermostate():

    def __init__(self, loop_delay=1):

        self.loop_delay = loop_delay

        # Pins

        self.led = Pin(2, Pin.OUT)

    def works(self):
        self.led.value(1)
        sleep(2)
        self.led.value(0)

    def start(self):
        while True:
            self.works()
            sleep(self.loop_delay)
