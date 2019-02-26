import spidev

class ADC:
    """
    class for gathering data from MCP300x IC via SPI
    """
    def __init__(self, CS):
        self.cs = max(0, min(1, CS))
        self.spi = spidev.SpiDev()
        self.bus = 0 # default is 0, but can be 1 if user enabled second bus
        # open a handle to the SPI bus using the CS
        self.spi.open(self.bus, self.cs)
        self.result = bytearray(3)

    def mcp3002(self, channel, debug = False):
        # check proper range for analog channel (0 or 1 on MCP3002)
        channel = max(0, min(1, channel))
        # gather data after sending data. *see spi_xfer2(args)
        # data output format = [1, (channel in 1 bits shifted to 8 bit length), 0]
        self.result = self.spi.xfer2([1, (2 + channel) << 6, 0], 50000)
        if debug: printRawResult(self.result)
        # return data from chip (last 10 bits of resulting bytearray)
        return ((self.result[1] & 3) << 8) + self.result[2]
    # end read mcp3002

    def mcp3004(self, channel, debug = False):
        # check proper range for analog channel (0 to 3 on MCP3004)
        channel = max(0, min(3, channel))
        # gather data after sending data. *see spi_xfer2(args)
        # data output format = [1, (channel in 3 bits shifted to 8 bit length), 0]
        self.result = self.spi.xfer2([1, (8 + channel) << 4, 0], 50000)
        if debug: printRawResult(self.result)
        # return data from chip (last 10 bits of resulting bytearray)
        return ((self.result[1] & 3) << 8) + self.result[2]
    
    def mcp3008(self, channel, debug = False):
        # check proper range for analog channel (0 to 7 on MCP3008)
        channel = max(0, min(7, channel))
        # gather data after sending data. *see spi_xfer2(args)
        # data output format = [1, (channel in 3 bits shifted to 8 bit length), 0]
        self.result = self.spi.xfer2([1, (8 + channel) << 4, 0], 50000)
        # print('result =', result)
        if debug: printRawResult(self.result)
        # return data from chip
        return ((self.result[1] & 3) << 8) + self.result[2]
    # end mcp3008

    def printRawResult(self, r):
        '''
        for debug purposes
        '''
        print(r[0], 'bytes =')
        for i in range(r[0]):
            print(bin(r[1][i]), end = ' ')
        println() # finish debug output with '\n'

    def __del__(self):
        self.spi.close()
        del self.cs, self.spi, self.bus, self.result
# end class ADC

# for testing. Adjust to suit your IC model (e.g. mcp3008 vs mcp3002)
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
    del adc
