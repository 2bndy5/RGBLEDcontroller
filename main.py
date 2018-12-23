from mcp300x import ADC
from colour import colour
from gpiozero import RGBLED

strip = RGBLED(13, 6, 5)
c = colour()
adc = ADC(0)

while True:
    try:
        h = adc.mcp3008(0)
        i = adc.mcp3008(1)
        c.setH(round(h / 1023.0 * 360))
        c.setI(i / 1023.0)
        #print("i_pot =", c.intensity, " h_pot =", c.hue, "\nRGB =", c.red, c.green, c.blue)
        strip.color = (c.red / 255.0, c.green / 255.0, c.blue / 255.0)
    except KeyboardInterrupt:
        break
#end infinite loop
