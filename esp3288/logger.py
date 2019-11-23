import utime as time


class Logger:

    def __init__(self):
        self.msg_format = "{date} - THERMOSTATE - [{level}] - {msg}"

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
            level=level,
            msg=msg
        )

    def process(self, msg):
        print(msg)

    def info(self, raw_msg):
        msg = self.get_msg(raw_msg, "INFO")
        self.process(msg)

    def warning(self, raw_msg):
        msg = self.get_msg(raw_msg, "WARNING")
        self.process(msg)

    def error(self, raw_msg):
        msg = self.get_msg(raw_msg, "ERROR")
        self.process(msg)

    def debug(self, raw_msg):
        msg = self.get_msg(raw_msg, "ERROR")
        self.process(msg)
