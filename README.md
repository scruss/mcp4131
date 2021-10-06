# mcp4131
MicroPython module to control MicroChip's MC4131 SPI digital potentiometer

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

## Hardware overview

The MCP4131 is a simple single-wiper 7-bit digital potentiometer controlled by an SPI interface. It has no memory settings, so will forget its current setting when it loses power.

Spec/Datasheet: [mcp4131 | Microchip Technology](https://www.microchip.com/en-us/product/MCP4131)

## Methods

### Creation

    m = mcp4131.MCP4131(s, cs)

Takes two arguments:

* *s*, an SPI object
* *cs*, a Pin object for the SPI Chip Select line.

Note that on initialization, the potentiometer is set mid-way (64).

### set

Set the potentiometer to a value between 0 .. 128, inclusive. Returns the value of the potentiometer:

    potval = m.set(0)
    
### get

Gets the potentiometer value, a number between 0 .. 128 inclusive.

    potval = m.get()

### inc

Increments the value of the wiper. Will not go past 128. Returns a value between 0 .. 128, inclusive. 

    potval = m.inc()

### dec

Decrements the value of the wiper. Will not go past 0. Returns a value between 0 .. 128, inclusive. 

    potval = m.dec()

### value

Synonym for **get()**.

    potval = m.value()
    
### ratio

Simlar to  **get()**, but returns a floating point value from 0.0 .. 1.0.

    potratio = m.ratio()

## Note / Caveat

The MCP4131 uses a multiplexed data in/data out pin. Reading the wiper value is quite cumbersone, so I maintain the current potentiometer wiper value in a parallel variable. **get()** and others merely return the value of this variable. 

## Author
© 2021, Stewart Russell, scruss.com
