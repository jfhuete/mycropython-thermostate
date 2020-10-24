from machine import RTC
from config.pins import PIN_LED_WIFI, PIN_LED_BOILER


class State:

    # Pins Out

    DAY_MODE = True
    NIGHT_MODE = False

    HYSTERESIS = 0.7

    def __init__(self):

        # Thermostate configuration

        self.date = RTC().datetime()

        self.temperature_setted = {
            self.DAY_MODE: 21,
            self.NIGHT_MODE: 17
        }

        self.summer = True

        self.day_mode_program = {
            0: [((0, 0), (23, 59))],  # Mon
            1: [((0, 0), (23, 59))],  # Tus
            2: [((0, 0), (23, 59))],  # Wen
            3: [((0, 0), (23, 59))],  # Thu
            4: [((0, 0), (23, 59))],  # Fri
            5: [((0, 0), (23, 59))],  # Sat
            6: [((0, 0), (23, 59))]   # Sun
        }

        self.mode = self.DAY_MODE

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
        self.__update_mode()
        self.__update_boiler_on()

    def __update_wifi_led(self):
        PIN_LED_WIFI.value(not self.wifi_connected)

    def __update_mode(self):

        if self.date is None:
            return

        weekday = self.date[3]
        now_hour = self.date[4]
        now_min = self.date[5]
        day_mode_intervals = self.day_mode_program[weekday]

        for interval in day_mode_intervals:

            hour_init = interval[0][0]
            min_init = interval[0][1]

            hour_finish = interval[1][0]
            min_finish = interval[1][1]

            now_major_init = now_hour > hour_init and now_min > min_init
            now_minor_finish = now_hour < hour_finish and now_min < min_finish

            if now_major_init and now_minor_finish:
                self.mode = self.DAY_MODE
                return

        self.mode = self.NIGHT_MODE

    def __update_boiler_on(self):

        initial_conditions = [
            self.temperature_measured is not None,
            self.date is not None
        ]

        if not all(initial_conditions):
            return

        conditions = [
            self.temperature_measured < self.temperature_setted[self.mode] + self.HYSTERESIS
        ]

        PIN_LED_BOILER.value(all(conditions))
