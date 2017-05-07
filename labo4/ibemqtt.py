import paho.mqtt.client as paho
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT) #left LED
GPIO.setup(13, GPIO.OUT) #right LED
GPIO.setup(15, GPIO.IN) #left button
GPIO.setup(16, GPIO.IN) #right button
GPIO.setup(18, GPIO.IN) #middle button

def writeKitchen(channel):
    write('l')
def writeLivingroom(channel):
    write('r')
def writeOff(channel):
    write('o')

def write(data):
    client.publish("home/groundfloor/livingroom/lights/lightx", str(data), qos=1)

def on_publish(client, userdata, mid):
    #   print("mid: "+str(mid))
    print("jow")

def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("home/groundfloor/kitchen/lights/lightx")

def on_message(client, userdata, message):
    print("Received message '" + str(message.payload) + "' on topic '" + message.topic + "' with QoS " + str(message.qos))
    if(str(message.payload) == "l"):
        GPIO.output(11, not GPIO.input(11))
    if(str(message.payload) == "r"):
        GPIO.output(13, not GPIO.input(13))
    if(str(message.payload) == "o"):
        GPIO.output(11, not GPIO.input(11))
        GPIO.output(13, not GPIO.input(13))

GPIO.add_event_detect(15, GPIO.RISING, callback=writeKitchen, bouncetime=500)

GPIO.add_event_detect(16, GPIO.RISING, callback=writeLivingroom, bouncetime=500)

GPIO.add_event_detect(18, GPIO.RISING, callback=writeOff, bouncetime=500)
def main():
    global client
    try:    
        client = paho.Client()
        client.on_publish = on_publish
        client.on_connect = on_connect
        client.on_message = on_message
        client.username_pw_set("bxaxrkah", "1zQixURXUYuB")
        client.connect("m10.cloudmqtt.com", 13915)
        client.loop_forever()
    except KeyboardInterrupt:
        pass
    finally:
        print("Programma afsluiten")
        GPIO.cleanup()
        client.loop_stop()
        client.disconnect()
if __name__ == "__main__":
    main()	
