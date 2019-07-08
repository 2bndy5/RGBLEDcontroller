# Import MPR121 module.
import time, board, neopixel, busio, adafruit_mpr121, paho.mqtt.client as mqtt, netifaces, socket
from colorsys import hsv_to_rgb as hsi2rgb, rgb_to_hsv as rgb2hsi
from .Ripple import *
# Create I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)
# Create MPR121 object.
mpr121 = adafruit_mpr121.MPR121(i2c)
# use to track cap sensor inputs
prevTouch = 0b0
edges = 0b0
held = 0b0

pixel_pin = board.A1
num_pixels = 12
# list of HSI colorspace data for each neopixel
leds = []
for i in range(num_pixels):
    leds.append(Pixel)
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.3, auto_write=False, pixel_order=(1, 0, 2, 3))

# hostname should define the MQTT topic like a physical domain
hostname = socket.getfqdn()
# replace legal delimiters with '/' char
topic = hostname.replace('.', '/')
topic = hostname.replace('-', '/')

# check for network connection
isConnected = False
for i in interfaces:
    addy = netifaces.ifaddresses(i)
    if addy.get(netifaces.AF_INET) != None and addy[netifaces.AF_INET][0]['addr'] != '127.0.0.1':
        print('connection found on device', i, '@', addy[netifaces.AF_INET][0]['addr'])
        isConnected = True
        myIP = addy[netifaces.AF_INET][0]['addr']
        break

# check for internet connection
isOnline = False
if isConnected:
    try:
        urllib.urlopen("https://www.google.com")
        isOnline = True
    except:
        isOnline = False

# create queue for ripple fx
q = fxQ(num_pixels) # max jobs & ripple segments == num_pixels

# trigger animation code for cycling through hue or fading to new color
for p in leds:
    p.tick()

# iterate existing queued fx jobs
for job in range(len(q)):
    result = q[job].fx()
    if result == None or result == True:
        triggers = q[job].wave
        for trig in triggers:
            leds[trig].cycleHue()
        if result == None:
            q.pop(q[job].start)

# find new jobs to push/pop in queue
# use binary 12-bit number where each bit is a pin
touch = mpr121.touched()
held = prevTouch & touch
edges = prevTouch ^ touch
for i in range(num_pixels):
    mask = 1 << i
    if edges & mask and touch & mask:
            q.push(i)

# finally draw changes to LEDs
for i, p in leds:
    rgb = hsi2rgb(p.hsi[0], p.hsi[1], p.hsi[2])
    rgb = (round(rgb[0] * 255), round(rgb[1] * 255), round(rgb[2] * 255))
    pixels[i] = (rgb[0], rgb[1], rgb[2])
# use this to display new color data
pixels.show()
# record last state for edge detection
prevTouch = touch
