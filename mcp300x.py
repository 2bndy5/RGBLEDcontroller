import pigpio

class ADC:
    """
    class for gathering data from MCP300x IC via SPI
    """
    def __init__(self, CS):
        self.pi = pigpio.pi()
        self.cs = max(0, min(1, CS))

    def mcp3002(self, channel):
        # check proper range for analog channel (0 or 1 on MCP3002)
        channel = max(0, min(1, channel))
        # create handle for use with pigpio spi functions
        self.adc = self.pi.spi_open(self.cs, 50000)
        # gather data after sending data. *see spi_xfer(args)
        # binary data output format = 1(channel in 1 bit)0
        result = self.pi.spi_xfer(self.adc, [1, (2 + channel) << 6, 0])
        # now delete handle
        self.pi.spi_close(self.adc)
        # return data from chip
        return (result[1][1] << 8) | result[1][2]

    def mcp3004(self, channel):
        # check proper range for analog channel (0 to 3 on MCP3004)
        channel = max(0, min(3, channel))
        # create handle for use with pigpio spi functions
        self.adc = self.pi.spi_open(self.cs, 50000)
        # gather data after sending data. *see spi_xfer(args)
        # binary data output format = 1(channel in 3 bits)0
        result = self.pi.spi_xfer(self.adc, [1, (8 + channel) << 4, 0])
        # now delete handle
        self.pi.spi_close(self.adc)
        # return data from chip
        return (result[1][1] << 8) | result[1][2]
    
    def mcp3008(self, channel):
        # check proper range for analog channel (0 to 7 on MCP3008)
        channel = max(0, min(7, channel))
        # create handle for use with pigpio spi functions
        self.adc = self.pi.spi_open(self.cs, 50000)
        # gather data after sending data. *see spi_xfer(args)
        # binary data output format = 1(channel in 3 bits)0
        result = self.pi.spi_xfer(self.adc, [1, (8 + channel) << 4, 0])
        # now delete handle
        self.pi.spi_close(self.adc)
        # return data from chip
        return (result[1][1] << 8) | result[1][2]
    
    def __del__(self):
        self.pi.stop()
        del self.pi, self.cs
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
