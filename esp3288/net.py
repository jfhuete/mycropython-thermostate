from config import WIFI_SSID, WIFI_PASS
import network


class Net:

    def __init__(self):
        self.wlan = network.WLAN(network.STA_IF)
        self.ap = network.WLAN(network.AP_IF)

    def connect(self, ssid=None, password=None):

        if self.wlan.isconnected():
            return

        self.wlan.active(True)
        self.ap.active(False)

        ssid = WIFI_SSID if ssid is None else ssid
        password = WIFI_PASS if password is None else password

        self.wlan.connect(ssid, password)

        while not self.wlan.isconnected():
            pass
