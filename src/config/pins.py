from machine import Pin

# In

PIN_TEMP_SENSOR = Pin(4, Pin.IN)
PIN_ON_OFF_BUTTON = Pin(14, Pin.IN, Pin.PULL_UP)

# Out

PIN_LED_WIFI = Pin(2, Pin.OUT)
PIN_LED_BOILER = Pin(5, Pin.OUT)
