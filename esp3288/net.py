import network
import time
from config import WIFI_SSID, WIFI_PASS


class Net:

    STATUS = [
        "Idle status",
        "Connecting with wifi",
        "Wrong password",
        "Access point not found",
        "Unknow problem when connecting",
        "Connected"
    ]

    def __init__(self):
        self.wlan = network.WLAN(network.STA_IF)
        self.ap = network.WLAN(network.AP_IF)

    def status(self):
        return self.STATUS[self.wlan.status()]

    def connect(self, ssid=None, password=None):
        """
        Connect to WIFI:

        :param ssid: ssid for the wifi network
        :param password: password for the wifi network

        :return: return tuple with boolean is connected and integer status
        """

        if self.wlan.isconnected():
            return self.wlan.isconnected(), self.status()

        self.wlan.active(True)
        self.ap.active(False)

        ssid = WIFI_SSID if ssid is None else ssid
        password = WIFI_PASS if password is None else password

        self.wlan.connect(ssid, password)

        while self.wlan.status() < self.wlan.STAT_CONNECTING:
            time.sleep(1)

        return self.wlan.isconnected(), self.status()
