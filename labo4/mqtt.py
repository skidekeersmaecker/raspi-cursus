import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import time

GPIO.setmode(GPIO.BOARD)

#leds
ledKitchen = 16
ledLivingroom = 18
GPIO.setup(ledKitchen, GPIO.OUT)
GPIO.output(ledKitchen, False)
GPIO.setup(ledLivingroom, GPIO.OUT)
GPIO.output(ledLivingroom, False)

#buttons
buttonMaster = 11
buttonKitchen = 13
buttonLivingroom = 15
GPIO.setup(buttonMaster, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(buttonKitchen, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(buttonLivingroom, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def callMaster(channel):
    print("called master button")
    write('master')

def callKitchen(channel):
    print("called kitchen button")
    write('kitchen')

def callLivingroom(channel):
    print("called livingroom button")
    write('livingroom')


#WIFI:
def write(data):
    mqttc.publish("home/groundfloor/kitchen/lights/lightx", str(data), qos=1)
    #mqttc.publish("home/groundfloor/livingroom/lights/lightx", str(data), qos=1)

#def on_connect(mqttc, obj, flags, rc):
def on_connect(mqttc, obj, rc): 
    print("connected: " + str(rc))
    mqttc.subscribe("home/groundfloor/livingroom/lights/lightx")
    #mqttc.subscribe("home/groundfloor/kitchen/lights/lightx")

def on_message(mqttc, obj, msg):
    print("msg: " + str(msg.payload) + " at topic: " + msg.topic + " with QoS: " + str(msg.qos))
    if(str(msg.payload) == "master"):
        GPIO.output(ledKitchen, not GPIO.input(ledKitchen))
        GPIO.output(ledLivingroom, not GPIO.input(ledLivingRoom))
    if(str(msg.payload) == "kitchen"):
        GPIO.output(ledKitchen, not GPIO.input(ledKitchen))
    if(str(msg.payload) == "livingroom"):
        GPIO.output(ledLivingroom, not GPIO.input(ledLivingroom))
 
def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))
    #mqttc.publish("home/groundfloor/kitchen/lights/lightx", str(data), qos=1)
    #test

GPIO.add_event_detect(buttonMaster, GPIO.FALLING, callback=callMaster, bouncetime=300)
GPIO.add_event_detect(buttonKitchen, GPIO.FALLING, callback=callKitchen, bouncetime=300)
GPIO.add_event_detect(buttonLivingroom, GPIO.FALLING, callback=callLivingroom, bouncetime=300)

def main():
    global mqttc
    try:
        mqttc = mqtt.Client()
        mqttc.on_publish = on_publish
        mqttc.on_connect = on_connect
        mqttc.on_message = on_message
        mqttc.username_pw_set("bxaxrkah", "1zQixURXUYuB")
        mqttc.connect("m10.cloudmqtt.com", 13915)
        mqttc.loop_forever()
    except KeyboardInterrupt:
        print("exiting program")
        mqttc.loop_stop()
        mqttc.disconnect()
        GPIO.cleanup()


if __name__ == "__main__":
    main()
