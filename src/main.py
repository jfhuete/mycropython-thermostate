from thermostate import Thermostate
from net import Net


if __name__ == "__main__":
    n = Net()
    n.connect()
    app = Thermostate()
    app.start()
