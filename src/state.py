from machine import Pin


class State:

    # Pins Out
    PIN_LED_WIFI = Pin(2, Pin.OUT)
    PIN_ENABLE_BOILER = None

    def __init__(self):

        # Thermostate configuration

        self.date = None

        self.temperature_setted = {
            "day": None,
            "night": None
        }

        self.summer = True

        self.time_on = {
            "monday": [],
            "tuesday": [],
            "wednesday": [],
            "thursday": [],
            "friday": [],
            "saturday": [],
            "sunday": []
        }

        self.force_on = False

        # Thermostate sensors

        self.__wifi_conected = False
        self.wifi_ssid = None
        self.wifi_state = None
        self.temperature_measured = None
        self.humidity_measured = None
        self.on_button = False

    @property
    def wifi_connected(self):
        return self.__wifi_connected

    @wifi_connected.setter
    def wifi_connected(self, value):
        self.__wifi_connected = value[0]
        self.wifi_ssid = value[2]
        self.wifi_state = value[2]

        self.__update_state()

    # Update actuators

    def __update_state(self):
        self.__update_wifi_led()
        self.__update_boiler_on()

    def __update_wifi_led(self):
        # value = 0 if  else 1
        self.PIN_LED_WIFI.value(not self.wifi_connected)

    def __update_boiler_on(self):
        pass
