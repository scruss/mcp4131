"""
micropython mcp4131 inc/dec test - scruss, 2021-10
"""

from machine import Pin, ADC, SPI
import mcp4131
import time
a = ADC(0)
cs = Pin(17, Pin.OUT)
s = SPI(0, sck=Pin(18), mosi=Pin(19), miso=Pin(16))
m = mcp4131.MCP4131(s, cs)

potval = m.set(0)
direction = 1
while True:
    time.sleep(.1)
    v = a.read_u16()
    print("[ %5.3f %5.3f %5.3f ]" % (0.0, 3.3*v/65536, 3.3))
    if direction == 1:
        potval = m.inc()
    else:
        potval = m.dec()
    if potval == 128:
        direction = -1
    if potval == 0:
        direction = 1
