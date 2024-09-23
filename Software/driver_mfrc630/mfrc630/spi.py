import spidev
import RPi.GPIO as GPIO

class SpiNotSelectedError(Exception):
    pass

class SpiHw:
    def __init__(self, bus=0, device=0, spd=1000000):
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = spd
        self.xfer = self.spi.xfer2
    
    def adquire(self):
        pass

    def release(self):
        pass

class SpiGpio:
    def __init__(self, spi_hw, pin_cs):
        self.spi = spi_hw
        self.pin_cs = pin_cs
        self.selected = False
        GPIO.setup(pin_cs, GPIO.OUT)
        GPIO.output(pin_cs, 1)

    def xfer(self, data):
        if not self.selected:
            raise SpiNotSelectedError("SPI not selected")
        return self.spi.xfer(data)

    # TODO: locks
    def adquire(self):
        self.selected = True
        GPIO.output(self.pin_cs, 0)

    def release(self):
        self.selected = False
        GPIO.output(self.pin_cs, 1)

class SpiShift:
    def __init__(self, spi_hw, shift, n):
        self.spi = spi_hw
        self.shift = shift
        self.n = n
        self.selected = False

    def xfer(self, data):
        if not self.selected:
            raise SpiNotSelectedError("SPI not selected")
        return self.spi.xfer(data)

    def adquire(self):
        self.selected = True
        self.shift.select(self.n)

    def release(self):
        self.selected = False
        self.shift.clear()