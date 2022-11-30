import utime as time
from config import LOGGER_LEVEL


class Logger:

    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3

    def __init__(self, state, module):
        self.state = state
        self.module = module
        self.msg_format = "{date} - THERMOSTATE:{module} - [{level}] - {msg}"

    def date_string(self):
        (y, m, d, h, M, s, _, _) = time.localtime()

        return "{d}-{m}-{y} {h}:{M}:{s}".format(
            y=y,
            m=m,
            d=d,
            h=h,
            M=M,
            s=s,
        )

    def get_msg(self, msg, level):
        return self.msg_format.format(
            date=self.date_string(),
            module=self.module,
            level=level,
            msg=msg
        )

    def process(self, msg):
        print(msg)

    def info(self, raw_msg):
        if LOGGER_LEVEL <= self.INFO:
            msg = self.get_msg(raw_msg, "INFO")
            self.process(msg)

    def warning(self, raw_msg):
        if LOGGER_LEVEL <= self.WARNING:
            msg = self.get_msg(raw_msg, "WARNING")
            self.process(msg)

    def error(self, raw_msg):
        if LOGGER_LEVEL <= self.ERROR:
            msg = self.get_msg(raw_msg, "ERROR")
            self.process(msg)

    def debug(self, raw_msg):
        if LOGGER_LEVEL <= self.DEBUG:
            msg = self.get_msg(raw_msg, "DEBUG")
            self.process(msg)
