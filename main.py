#from mcp300x import ADC
from colour import colour
from gpiozero import RGBLED, MCP3008

strip = RGBLED(13, 6, 5)
c = colour()
#adc = ADC(0)
adc = []
adc[0] = MCP3008(0)
adc[1] = MCP3008(1)

while True:
    try:
        c.setH(round(adc[0].value * 360))
        c.setI(adc[1].value)
        strip.color = (c.red / 255.0, c.green / 255.0, c.blue / 255.0)
    except KeyboardInterrupt:
        break
#end infinite loop