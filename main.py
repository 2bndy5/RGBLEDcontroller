from mcp300x import ADC
# from colour import colour
from gpiozero import RGBLED
import paho.mqtt.client as mqtt
import colorsys
import time

broker="B-Pi3"
topic = "test/led"
client = mqtt.Client(client_id="")
rgb = (0, 0, 0)

def hollaBroker():
    try:
        client.connect(broker)
    except TimeoutError as t_err:
        print("**connection attempt with broker timed out!")
        return False
    finally:
        client.subscribe(topic, qos=2)
        print("**Connected to ", broker, " and subscribed to \"", topic, "\"", sep='')
        return True

def on_message(client, userdata, message):
    msg = str(message.payload.decode("utf-8"))
    print("message received " , msg)
    # print("message topic=",message.topic)
    # print("message qos=",message.qos)
    # print("message retain flag=",message.retain)
    red = 0
    green = 0
    blue = 0
    if (msg.find("#") == 0):
        if (len(msg) == 4):
            red = int(msg[1] + msg[1], 16)
            green = int(msg[2] + msg[2], 16)
            blue = int(msg[3] + msg[3], 16)
        else:
            red = int(msg[1] + msg[2], 16)
            green = int(msg[3] + msg[4], 16)
            blue = int(msg[5] + msg[6], 16)
    elif (msg.find(",") > 0):
        e1 = msg.find(",")
        red = int(msg[: e1])
        e2 = msg.find(",", e1 + 1)
        green = int(msg[e1 + 1 : e2])
        blue = int(msg[e2 + 1 :])
        del e1, e2
    print(red, green, blue, sep=",")
    red = float(red / 255.0)
    green = float(green / 255.0)
    blue = float(blue / 255.0)
    global rgb
    rgb = (red, green, blue)
    del red, green, blue
    
client.on_message = on_message

strip = RGBLED(13, 6, 5)
adc = ADC(0)
last_hPot = 0
last_iPot = 0
connected = hollaBroker()

while connected:
    try:
        client.loop_start()
        hPot = adc.mcp3008(0)
        iPot = adc.mcp3008(1)
        sat =  0.0
        if (hPot >= 1022):
            sat = 0.0
        else:
            sat = 1.0
        if (abs(hPot - last_hPot) >=2 or abs(iPot - last_iPot) >= 2):
            rgb = colorsys.hsv_to_rgb(hPot / 1023.0, sat, iPot / 1023.0)
            last_hPot = hPot
            last_iPot = iPot

        #client.publish(topic, "#" + "{:02X}".format(round(rgb[0] * 255)) + "{:02X}".format(round(rgb[1] * 255)) + "{:02X}".format(round(rgb[2] * 255)))

        time.sleep(0.5)
        client.loop_stop()
        strip.color = (rgb[0], rgb[1], rgb[2])
        print("RGB =", rgb[0], rgb[1], rgb[2])
    except KeyboardInterrupt:
        client.disconnect()
        client.loop_stop()
        break
    time.sleep(0.5)
#end infinite loop
