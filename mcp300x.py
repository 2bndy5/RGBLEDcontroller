import spidev
import RPi.GPIO as GPIO
 
class ADC:
    """
    class for gathering data from MCP300x IC via SPI
    """
    def __init__(self, CS):
        self.cs = max(0, min(1, CS))
        GPIO.setmode(GPIO.BCM)
        # set up the SPI interface pins
        GPIO.setup(10, GPIO.OUT)            # MOSI pin
        GPIO.setup(9, GPIO.IN)              # MISO pin
        GPIO.setup(11, GPIO.OUT)            # CLK pin
        GPIO.setup(8 - self.cs, GPIO.OUT)   # CS pin (CE0 | CE1) -> CE == 0 ? 8 : 7
        # create object for handling SPI interface with spidev
        self.spi = spidev.SpiDev()
        bus = 0 # default is 0, but can be 1 if user enabled second bus

    def mcp3002(self, channel):
        # check proper range for analog channel (0 or 1 on MCP3002)
        channel = max(0, min(1, channel))
        # open a handle to the SPI bus using the CS
        self.spi.open(bus, self.cs)
        # set CLK speed to 50kHz according to datasheet
        self.spi.max_speed_hz = 50000
        # spidev docs mandate CS pin pulled low during xfer2() and then high afterward
        GPIO.output(8 - self.cs, False)
        # gather data after sending data. *see spi_xfer2(args)
        # data output format = [1, (channel in 1 bits shifted to 8 bit length), 0]
        result = self.spi.xfer2([1, (2 + channel) << 6, 0])
        GPIO.output(8 - self.cs, True)
        # now delete handle
        self.spi.close()
        # return data from chip (last 10 bits of resulting bytearray)
        return (result[1][1] << 8) | result[1][2]

    def mcp3004(self, channel):
        # check proper range for analog channel (0 to 3 on MCP3004)
        channel = max(0, min(3, channel))
        # open a handle to the SPI bus using the CS
        self.spi.open(bus, self.cs)
        # set CLK speed to 50kHz according to datasheet
        self.spi.max_speed_hz = 50000
        # spidev docs mandate CS pin pulled low during xfer2() and then high afterward
        GPIO.output(8 - self.cs, False)
        # gather data after sending data. *see spi_xfer2(args)
        # data output format = [1, (channel in 3 bits shifted to 8 bit length), 0]
        result = self.spi.xfer2([1, (8 + channel) << 4, 0])
        GPIO.output(8 - self.cs, True)
        # now delete handle
        self.spi.close()
        # return data from chip (last 10 bits of resulting bytearray)
        return (result[1][1] << 8) | result[1][2]
    
    def mcp3008(self, channel):
        # check proper range for analog channel (0 to 7 on MCP3008)
        channel = max(0, min(7, channel))
        # open a handle to the SPI bus using the CS
        self.spi.open(bus, self.cs)
        # set CLK speed to 50kHz according to datasheet
        self.spi.max_speed_hz = 50000
        # spidev docs mandate CS pin pulled low during xfer2() and then high afterward
        GPIO.output(8 - self.cs, False)
        # gather data after sending data. *see spi_xfer2(args)
        # data output format = [1, (channel in 3 bits shifted to 8 bit length), 0]
        result = self.spi.xfer2([1, (8 + channel) << 4, 0])
        GPIO.output(8 - self.cs, True)
        # now delete handle
        self.spi.close()
        # return data from chip (last 10 bits of resulting bytearray)
        return (result[1][1] << 8) | result[1][2]
    
    def __del__(self):
        spi.close() # in case of KeyboardInterrupt
        del self.cs
# end class ADC

if __name__ == "__main__":
    adc = ADC(0)
    print('channel 1 =', adc.mcp3008(0))
    print('channel 2 =', adc.mcp3008(1))
    print('channel 3 =', adc.mcp3008(2))
    print('channel 4 =', adc.mcp3008(3))
    print('channel 5 =', adc.mcp3008(4))
    print('channel 6 =', adc.mcp3008(5))
    print('channel 7 =', adc.mcp3008(6))
    print('channel 8 =', adc.mcp3008(7))
