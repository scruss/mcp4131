"""
MicroPython driver for a MCP4131 digital potentiometer.
Requires an SPI bus and a CS pin.

scruss, 2021-10

limited command set: set, get, inc, dec

"""

from micropython import const

_CMD_INCREMENT = const(0x04)    # b00000100 - Increment Wiper
_CMD_DECREMENT = const(0x08)    # b00001000 - Decrement Wiper
_CMD_WRITE = const(0x00)       # b00000011 11111111 - Write Data
# can't get read to work
_CMD_READ = const(0x0f)        # b00001111 11111111 - Read  Data


class MCP4131:
    def __init__(self, spi, cs):
        self.spi = spi
        self.cs = cs
        self.spi.init()
        self.val = 64  # initialize at mid-range
        self.set(self.val)

    def set(self, v):
        self.val = v
        if self.val > 128:
            self.val = 128
        if self.val < 0:
            self.val = 0
        self.cs.value(0)
        self.spi.write(bytes([_CMD_WRITE, self.val]))
        self.cs.value(1)
        return(self.val)

    def get(self):
        return(self.val)

    def value(self):
        return(self.val)

    def ratio(self):
        return(self.val / 128.0)

    def inc(self):
        self.cs.value(0)
        self.spi.write(bytes([_CMD_INCREMENT]))
        self.cs.value(1)
        self.val = self.val + 1
        if self.val > 128:
            self.val = 128
        return(self.val)

    def dec(self):
        self.cs.value(0)
        self.spi.write(bytes([_CMD_DECREMENT]))
        self.cs.value(1)
        self.val = self.val - 1
        if self.val < 0:
            self.val = 0
        return(self.val)
