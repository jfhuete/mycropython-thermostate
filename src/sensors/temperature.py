import dht
from logger import Logger
from config.pins import PIN_TEMP_SENSOR


class Temperature:

    MEASSURES_LEN = 50

    def __init__(self, state):
        self.state = state
        self.sensor = dht.DHT22(PIN_TEMP_SENSOR)
        self.logger = Logger(self.state, "TEMP")

        self.__temp_meassures = []
        self.__humidity_meassures = []

    def measure(self):
        try:
            self.sensor.measure()

            temp = self.sensor.temperature()
            humidity = self.sensor.humidity()

            self.__add_temperature(temp, humidity)

            temp_mean = self.__get_temperature()
            humidity_mean = self.__get_humidity()

            self.logger.info("Temp: {} ºC, Humid: {}%".format(
                temp_mean, humidity_mean))
        except OSError as e:
            temp_mean = None
            humidity_mean = None
            self.logger.error("Can't to read temperature {}".format(e))

        self.state.temperature_measured = temp_mean
        self.state.humidity_measured = humidity_mean

    def __add_temperature(self, temp, humidity):

        self.__temp_meassures.append(temp)
        self.__humidity_meassures.append(humidity)

        if len(self.__temp_meassures) > self.MEASSURES_LEN:
            self.__temp_meassures.pop(0)

        if len(self.__humidity_meassures) > self.MEASSURES_LEN:
            self.__humidity_meassures.pop(0)

    def __get_temperature(self):

        acum = 0

        for temp in self.__temp_meassures:
            acum += temp

        return round(acum / len(self.__temp_meassures), 2)

    def __get_humidity(self):

        acum = 0

        for humidity in self.__humidity_meassures:
            acum += humidity

        return round(acum / len(self.__humidity_meassures), 2)
