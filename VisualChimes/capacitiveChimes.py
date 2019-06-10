import time
import board
import neopixel
import busio
from colorsys import hsv_to_rgb as hsi2rgb
from .Ripple import Ripple, fxQ

# Import MPR121 module.
import adafruit_mpr121
# Create I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)
# Create MPR121 object.
mpr121 = adafruit_mpr121.MPR121(i2c)

 
pixel_pin = board.A1
num_pixels = 12
# list of HSI colorspace data for each neopixel
hsi = []
for i in range(num_pixels):
    hsi.append([0.0, 1.0, 0.0])
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.3, auto_write=False,
                           pixel_order=(1, 0, 2, 3))
# use this to set color data
rgb = hsi2rgb(hsi[i][0], hsi[1], hsi[2])
rgb = (round(rgb[0] * 255), round(rgb[1] * 255), round(rgb[2] * 255))
pixels[i] = (rgb[0], rgb[1], rgb[2])
# use this to display new color data
pixels.show()

# create queue for ripple fx
q = fxQ(num_pixels) # max jobs & ripple segments == num_pixels

"""
    # use for each individual pads
    for i in range(12):
        # Call is_touched and pass it then number of the input.  If it's touched
        # it will return True, otherwise it will return False.
        if mpr121[i].value:
            touched = i

    # or use tuple of booleans for each pin
    touched = mpr121.touched_pins

    # or use binary 12-bit number where each bit is a pin
    touch = mpr121.touched()
    # edges = prevTouch ^ touch
    # held = prevTouch & touch
"""
edges = 0; held = 0

# do something to form queue of ripples
# iterate existing queued fx jobs, then add new jobs to queue, then draw LEDs
prevTouch = touch

ripple = Ripple(0, num_pixels)

def go2norm(i):
	if ((not effect.royGbiv and (hsi[i][0] >= 300/360.0)) or effect.royGbiv):
		c = int(hsi[i][2] * 255)
		if ((effect.royGbiv and c >= 128)):
			hsi[i].setColorI(c-11) 
		elif (int(c)):
			hsi[i].setColorI(0)
		else: return bool(int(c))
	else: return False	

# checks neopixels' hue value and increments (by 30 if hue <= 330) through spectrum
def cycleHue(i):
	tempH = int(hsi[i][0] * 360)
	if tempH <= 330:
		hsi[i][0] = (tempH + 30) / 360.0
	else: hsi[i][0] = 0

def setAllI(x): # where x == float [0,1]
	for i in range(num_pixels):
		hsi[i][2] = x
