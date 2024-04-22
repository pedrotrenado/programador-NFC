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

class MFRC630:
    def __init__(self, spi, pin_cs):
        self.spi = spi
        self.pin_rst = pin_cs
        GPIO.setup(pin_cs, GPIO.OUT)
        GPIO.output(pin_cs, 1)

    def xfer(self, data):
        if not self.selected:
            raise SpiNotSelectedError("SPI not selected")
        return self.spi.xfer(data)
    
    def select(self):
        self.selected = True
        GPIO.output(self.pin_cs, 0)

    def deselect(self):
        self.selected = False
        GPIO.output(self.pin_cs, 1)

    def read_reg(self, reg):
        cmd = [reg & 0x7F, 0]
        self.select()
        res = self.xfer(cmd)
        self.deselect()
        return res[1]
    
    def write_reg(self, reg, val):
        cmd = [reg | 0x80, val]
        self.select()
        self.xfer(cmd)
        self.deselect()

    def cmd_auth(self, key_type, block,uid):
        cmd = [0x60, key_type, block] + uid
        self.select()
        self.xfer(cmd)
        self.deselect()

    def cmd_transceive(self, data, lenght):
        cmd = [0x07] + data[:lenght]
        self.select()
        res = self.xfer(cmd)
        self.deselect()
        return res[1:]
                   
    def cmd_idle(self):
        cmd = [0x0E]
        self.select()
        self.xfer(cmd)
        self.deselect()

    def flush_fifo(self):
        cmd = [0x02, 0x80]
        self.select()
        self.xfer(cmd)
        self.deselect()
    


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