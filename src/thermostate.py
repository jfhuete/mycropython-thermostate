from machine import RTC
import ntptime

from time import sleep

from state import State
from logger import Logger
from net import Net

from sensors.temperature import Temperature


class Thermostate():

    # Loop delay in seconds
    LOOP_DEALY = 1

    def __init__(self):

        self.loop_delay = self.LOOP_DEALY

        # Modules
        self.state = State()
        self.net = Net(self.state)
        self.logger = Logger(self.state, "LOOP")

        # Sensors
        self.temp_sensor = Temperature(self.state)

        # Initialized
        self.connect_wifi
        self.set_time()

    # Configuration methods

    def connect_wifi(self):
        if not self.net.connected:
            self.net.connect()

    def set_time(self):

        # Sync date if date is None or each hour in first 5 seconds

        date_sync = self.state.date is None or \
            (self.state.date[5] == 0 and self.state.date[6] < 5)

        if not date_sync:
            self.state.date = RTC().datetime()
            return

        if self.net.connected:
            try:
                self.logger.info("Setting local date")
                ntptime.settime()
                self.state.date = RTC().datetime()
                self.logger.info("Date setted: {}".format(self.state.date))
            except OSError as error:
                self.logger.error(
                    "Can't to set local time. {}".format(error))
        else:
            self.logger.error(
                "Can't to set local time. Network is not connected")

    # Update state

    def update_state(self):
        self.connect_wifi()
        self.set_time()

        # Read sensors

        self.temp_sensor.measure()

    # Loop method

    def start(self):
        try:
            while True:
                self.update_state()
                sleep(self.loop_delay)
        except KeyboardInterrupt:
            self.net.disconnect()
