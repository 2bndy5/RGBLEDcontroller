from mcp300x import ADC
from colour import colour
from gpiozero import RGBLED

strip = RGBLED(13, 6, 5)
c = colour()
adc = ADC(0)

while True:
    try:
        c.setH(round(adc.mcp3008(0) / 1023.0 * 360))
        c.setI(round(adc.mcp3008(1) / 1023.0))
        strip.color = (c.red / 255.0, c.green / 255.0, c.blue / 255.0)
    except KeyboardInterrupt:
        break
#end infinite loop