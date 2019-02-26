import time
from colorsys import hsv_to_rgb, rgb_to_hsv
from math import floor

from gpiozero import RGBLED, MCP3008

import paho.mqtt.client as mqtt

rgb = (0, 0, 0)

broker="B-Pi3"
topic = "test/led"
client = mqtt.Client(client_id="")
isListening = False
offTime = 0

def hollaBroker():
    try:
        client.connect(broker)
    except TimeoutError as t_err:
        print("**connection attempt with broker timed out!")
        return False
    finally:
        client.subscribe(topic, qos=2)
        print("**Connected to", broker, "and subscribed to", topic)
        return True

def on_message(client, userdata, message):
    msg = str(message.payload.decode("utf-8"))
    # print("message received " , msg)
    # print("message topic=",message.topic)
    # print("message qos=",message.qos)
    # print("message retain flag=",message.retain)
    red = 0
    green = 0
    blue = 0
    if (msg.find("#") == 0):    # using html hexadecimal notation
        if (len(msg) == 4):     # using shorthand hex '#fff'
            red = int(msg[1] + msg[1], 16)
            green = int(msg[2] + msg[2], 16)
            blue = int(msg[3] + msg[3], 16)
        else:                   # using standard hex '#ffffff'
            red = int(msg[1] + msg[2], 16)
            green = int(msg[3] + msg[4], 16)
            blue = int(msg[5] + msg[6], 16)
    elif (msg.find(",") > 0):   # using 'R,G,B' notation
        e1 = msg.find(",")
        red = int(msg[: e1])
        e2 = msg.find(",", e1 + 1)
        green = int(msg[e1 + 1 : e2])
        blue = int(msg[e2 + 1 :])
        del e1, e2
    elif (msg.find(".") > 0):   # using 'Hue Sat Val' float values
        e1 = msg.find(" ")
        red = float(msg[: e1])              # used as Hue
        e2 = msg.find(" ", e1 + 1)
        green = float(msg[e1 + 1 : e2])     # used as Saturaion
        blue = float(msg[e2 + 1 :])         # used as Intensity (AKA Value/Lumens)
        del e1, e2
        # now get actual RGB from HSV values using colorsys function
        newC = hsv_to_rgb(red, green, blue)
        red = newC[0] * 255.0
        green = newC[1] * 255.0
        blue = newC[2] * 255.0
        del newC

    # print(red, green, blue, sep=",")
    red = float(red / 255.0)
    green = float(green / 255.0)
    blue = float(blue / 255.0)
    global rgb              # needed to merge data into stream
    rgb = (red, green, blue)
    del red, green, blue
    
client.on_message = on_message

strip = RGBLED(13, 6, 5)    # define GPIO pins for led
connected = hollaBroker()   # is broker found

def applyPots():
    hPot = MCP3008(0)   # create hue pot object
    iPot = MCP3008(1)   # create intensity pot object
    tempH = hPot.value
    tempI = iPot.value
    sat =  0.0
    if (tempH > 1020):
        sat = 0.0
    else:
        sat = 1.0
    print('h =', tempH , '\ni =', tempI)
    tempC = hsv_to_rgb(tempH, sat, tempI)
    client.publish(topic, repr(round(tempC[0] * 255)) + "," + repr(round(tempC[1] * 255)) + "," + repr(round(tempC[2] * 255)))
    del tempC, tempH, tempI, hPot, iPot

while connected:
    try:
        sec = time.time()
        if (floor(sec) % 2 == 0):
            client.loop_start()
            isListening = True
            offTime = sec + 1.5
        elif (sec >= offTime and isListening): 
            client.loop_stop()
        applyPots()
        strip.color = rgb
        #print("RGB =", rgb[0], rgb[1], rgb[2])
    except KeyboardInterrupt:
        client.disconnect()
        client.loop_stop()
        break
    #time.sleep(0.5)
#end client connected loop
