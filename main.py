import time
from colorsys import hsv_to_rgb, rgb_to_hsv
import paho.mqtt.client as mqtt
from gpiozero import RGBLED, DigitalOutputDevice
import hsv_led

mainLight = False


broker = "openHABianpi"
topics = [
    ("bedroom/light", 0),
    ("bedroom/moodLights", 0),
    ("bedoroom/temperature", 0),
    ("bedroom/humidity", 0),
]
client = mqtt.Client(client_id="")
isListening = False
offTime = 0


def hollaBroker():
    try:
        client.connect(broker)
        # List of string and integer tuples: subscribe([("my/topic", 0), ("another/topic", 2)])
        client.subscribe(topics)
        print("**Connected to", broker, "and subscribed to", topic)
        return True
    except TimeoutError:
        print("**connection attempt with broker timed out!")
        return False


# takes a string in various formats and gathers HSI & RGB info
#   '#RGB' or '#RRGGBB' for html/hexadecimal format
#   'r,g,b' for red,green,blue format all in range [0,255]
#   'h.h,s.s,i.i' for hue[0,360],saturation[0,100],intensity[0,100] format
# returns a dictionary that contains:
#   'rgb': [ int(red), int(green), int(blue) ] all in range [0,255]
#   'hsi': [ float(hue), float(sat), float(intensity) ] all in range [0.0,1.0]
def parseColor(msg):
    rgb = [0, 0, 0]
    hsv = [0, 0, 0]
    isHex = msg.find("#")
    if isHex >= 0:  # using html hexadecimal notation
        if len(msg) - isHex == 3:  # using shorthand hex '#fff'
            rgb[0] = int((msg[isHex + 1] << 4) + msg[isHex + 1], 16)
            rgb[1] = int((msg[isHex + 2] << 4) + msg[isHex + 2], 16)
            rgb[2] = int((msg[isHex + 3] << 4) + msg[isHex + 3], 16)
        else:  # using standard hex '#ffffff'
            rgb[0] = int(msg[isHex + 1 : isHex + 2], 16)
            rgb[1] = int(msg[isHex + 3 : isHex + 4], 16)
            rgb[2] = int(msg[isHex + 5 : isHex + 6], 16)
        hsv = hsv_to_rgb(rgb[0] / 255.0, rgb[1] / 255.0, rgb[2] / 255.0)
    elif msg.find(".") > 0:  # using 'Hue,Sat,Val' float values
        msg = msg.rsplit(",")
        for i in range(3):
            if i < len(msg):
                if not i:
                    hsv[i] = float(msg[i]) / 360.0
                else:
                    hsv[i] = float(msg[i]) / 100.0
            else:
                hsv[i] = 0  # string was malformed
        # now get actual RGB from HSV values using colorsys function
        newC = hsv_to_rgb(rgb[0], rgb[1], rgb[2])
        for i in range(len(rgb)):
            rgb[i] = round(newC[i] * 255)
        del newC
    elif msg.find(",") > 0:  # using 'R,G,B' notation
        msg = msg.rsplit(",")
        for i in range(3):
            if i < len(msg):
                rgb[i] = int(msg[i])
            else:
                rgb[i] = 0  # string was malformed
        hsv = hsv_to_rgb(rgb[0] / 255.0, rgb[1] / 255.0, rgb[2] / 255.0)

    # print(rgb[0], rgb[1], rgb[2], sep=",")
    return {"rgb": rgb, "hsi": hsv}


def isON(msg):
    if msg.upper() == "ON":
        return True
    elif msg == "1":
        return True
    else:
        return False


def on_message(client, userdata, message):
    t = str(message.topic.decode("utf-8"))
    msg = str(message.payload.decode("utf-8"))
    # print("message topic=",message.topic)
    # print("message qos=",message.qos)
    # print("message received=", msg)
    # print("message retain flag=",message.retain)
    if t == topics[1][0]:
        global idleHSI  # needed to merge data into stream
        temp = parseColor(msg)  # save new color in ['rgb','hsi'] format
        idleHSI = temp["hsi"]
    elif t == topics[0][0]:
        global mainLight  # needed to merge data into stream
        mainLight = isON(msg)  # save new light command


client.on_message = on_message

light = DigitalOutputDevice(4)  # define GPIO pin for control relay
strip = RGBLED(13, 6, 5)  # define GPIO pins for led strip
strip_color = HSI_LED()

connected = hollaBroker()  # is broker found
while connected:
    try:
        sec = time.monotonic()
        if int(sec) % 2 == 0:
            client.loop_start()
            isListening = True
            offTime = sec + 1.5
        elif sec >= offTime and isListening:
            client.loop_stop()
        strip_color.tick()
        strip.value = (strip_color.rgb[0], strip_color.rgb[1], strip_color.rgb[2])
        light.value = mainLight
    except KeyboardInterrupt:
        client.disconnect()
        client.loop_stop()
        break
    # time.sleep(0.5)
# end client connected loop
