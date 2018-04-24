#!/usr/bin/python3

import paho.mqtt.subscribe as subscribe
import yeelight
import time
import json
import yeelight
#import bibliopixel.colors as colors

mqtt_topic = "milight/updates/0x168B/rgb_cct/3"
mqtt_host = "192.168.0.4"
mqtt_port = 1883
mqtt_username = "pi"
mqtt_password = "raspberry"
yeelight_ip = "192.168.0.7"
hue = 359
saturation = 100
bulb = yeelight.Bulb(yeelight_ip)
bulb.start_music()

def remap(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def query():
    msg = subscribe.simple(mqtt_topic, 
                   hostname=mqtt_host,
                   port=mqtt_port,
                   auth={'username':mqtt_username,
                   'password':mqtt_password})
    yeelight(msg.payload)               
#    print("%s %s" % (msg.topic, msg.payload))
#    yeelight(msg.payload)

def yeelight(payload):
    data = json.loads(str(payload, 'utf-8'))
#    import yeelight
#    bulb = yeelight.Bulb("192.168.42.40")
#    bulb.start_music()
    global saturation
    global hue
    if 'state' in data:
        if data['state'] == 'ON':
            bulb.turn_on()
        else:
            bulb.turn_off()
    
    if 'brightness' in data:
#        value = data['brightness']
#        value = remap(data['brightness'], 0, 1, 0, 255)
        bulb.set_brightness(remap(data['brightness'], 0, 255, 0, 100))
    
    if 'color_temp' in data:
        print(remap(data['color_temp'], 370, 153, 3055, 5555))
        bulb.set_color_temp(remap(data['color_temp'], 370, 153, 3055, 5555))
    
    if 'hue' in data:
        hue = data['hue']
#        hsv = hue,1.0,1.0
#        r,g,b = colors.hsv2rgb_360(hsv)
#        print(r,g,b)
#        bulb.set_rgb(r,g,b)
        bulb.set_hsv(hue,saturation)
        
    if 'saturation' in data:
        saturation = data['saturation']
        bulb.set_hsv(hue,saturation)

    print(payload)
    
    try:
        time.sleep(0.1)
    except yeelight.BulbException as ex:
        print("Unable to change the bulb: %s", ex)

while True:
    try:
        query()
    except Exception as exc:
        print("error: %s", exc)
#        time.sleep(15)
