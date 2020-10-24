import network
import time

from logger import Logger

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

    def __init__(self, state):

        self.state = state

        self.wlan = network.WLAN(network.STA_IF)
        self.ap = network.WLAN(network.AP_IF)

        self.ssid = None

        self.logger = Logger(self.state, "NET")

    def connect(self, ssid=None, password=None):
        """
        Connect to WIFI:

        :param ssid: ssid for the wifi network
        :param password: password for the wifi network

        :return: return tuple with boolean is connected and integer status
        """

        ssid = WIFI_SSID if ssid is None else ssid
        password = WIFI_PASS if password is None else password

        if self.wlan.isconnected():
            self.ssid = ssid
            return self.wlan.isconnected(), self.status

        self.logger.info("Trying to connect with {ssid}".format(ssid=ssid))

        self.wlan.active(True)
        self.ap.active(False)

        self.wlan.connect(ssid, password)

        while self.wlan.status() <= network.STAT_CONNECTING:
            time.sleep(1)

        if not self.wlan.isconnected():
            self.logger.error("Can't to connect with {ssid}: {problem}".format(
                ssid=ssid,
                problem=self.status
            ))
        else:
            self.logger.info("Connected with {ssid}".format(ssid=ssid))
            self.ssid = ssid

        self.state.wifi_connected = (
            self.wlan.isconnected(),
            self.ssid,
            self.status
        )

    def disconnect(self):
        if self.wlan.isconnected():
            self.wlan.disconnect()
            self.logger.info("Disconnected of {ssid}".format(ssid=self.ssid))
            self.state.wifi_connected = (
                self.wlan.isconnected(),
                None,
                self.status,
            )

    @property
    def status(self):
        return self.STATUS[self.wlan.status()]

    @property
    def connected(self):
        if self.wlan.isconnected():
            self.state.wifi_connected = (
                True,
                self.ssid,
                self.status,
            )
            return True
        else:
            self.state.wifi_connected = (
                False,
                None,
                self.status,
            )
            return False
