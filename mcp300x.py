import pigpio

class ADC:
    """
    class for gathering data from MCP300x IC via SPI
    """
    def __init__(self, CS):
        self.pi = pigpio.pi()
        self.cs = 0
        if CS > 1 or CS < 0:
            self.cs = 0
        else: self.cs = CS

    def mcp3002(self, channel):
        # check proper range for analog channel (0 or 1 on MCP3002)
        if channel > 1 or channel < 0:
            channel = 0
        # create handle for use with pigpio spi functions
        self.adc = self.pi.spi_open(self.cs, 50000)
        # gather data after sending data. *see spi_xfer(args)
        self.result = self.pi.spi_xfer(self.adc, [1, (2 + channel) << 6, 0])
        # for debug purposes
        # print(self.result)
        # for i in range(self.result[0]):
        #     print(bin(self.result[1][i]), end = ' ')
        # now delete handle
        self.pi.spi_close(self.adc)
        # return data from chip
        return self.result[1][1] >> 8 | self.result[1][2]
    # end adc2

    def mcp3008(self, channel):
        # check proper range for analog channel (0 to 7 on MCP3008)
        if channel > 7 or channel < 0:
            channel = 0
        # create handle for use with pigpio spi functions
        self.adc = self.pi.spi_open(self.cs, 50000)
        # gather data after sending data. *see spi_xfer(args)
        self.result = self.pi.spi_xfer(self.adc, [1, (2 + channel) << 6, 0])
        # for debug purposes
        # print(self.result)
        # for i in range(self.result[0]):
        #     print(bin(self.result[1][i]), end = ' ')
        # now delete handle
        self.pi.spi_close(self.adc)
        # return data from chip
        return self.result[1][1] >> 8 | self.result[1][2]

    # end adc8
    
    def __del__(self):
        self.pi.stop()
        del self.pi, self.cs
# end class ADC