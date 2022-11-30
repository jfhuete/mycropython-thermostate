from machine import Pin
from logger import Logger
from config.pins import PIN_ON_OFF_BUTTON


class onOffButton:

    def __init__(self, state):
        self.state = state
        self.logger = Logger(self.state, "ON_OFF_BUTTON")
        self.button = PIN_ON_OFF_BUTTON

        self.button.irq(
            trigger=Pin.IRQ_FALLING,
            handler=lambda p: self.on_off_boiler()
        )

    def on_off_boiler(self):

        self.state.on_button = not self.state.on_button
        self.logger.info(
            "On Off button pulsed: on_button {}".format(self.state.on_button))
