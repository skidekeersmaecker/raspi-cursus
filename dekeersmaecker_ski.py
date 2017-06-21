import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import time
import datetime

GPIO.setmode(GPIO.BOARD)

button = 11
led = 12

GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(led, GPIO.OUT)
GPIO.output(led, True)

aantalPersonen = 0
start = 0
end = 0
elapsed = 0

def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))

def on_connect(mqttc, userdata, rc):
    print("Connected with result code "+str(rc))
    mqttc.subscribe("examen")

def write(data):
    mqttc.publish("examen", str(data), qos=1)

def writeLogFile():
    global aantalPersonen
    line = str(aantalPersonen)
    f = open("logfile.log", "w")
    f.write(line)
    f.close()

def writeMqtt():
    f = open('logfile.log', 'r')
    lines = f.readlines()
    personen = lines[0]
    f.close()
    write(personen)


def hit(channel):
    global aantalPersonen
    global start
    global end
    elapsed = 0

    if GPIO.input(button) is 1:
        start = time.time()
    if GPIO.input(button) is 0:
        end = time.time()
        elapsed = end - start
        print("elapsed time: ")
        print(elapsed)
        if(elapsed >= 5):
            writeLogFile()
            writeMqtt()
        else:
            aantalPersonen+=1
            print("aantalPersonen: ")
            print(aantalPersonen)

GPIO.add_event_detect(button, GPIO.BOTH, callback=hit, bouncetime=200)

try:
    mqttc = mqtt.Client()
    mqttc.on_publish = on_publish
    mqttc.on_connect = on_connect
    #mqttc.on_message = on_message
    mqttc.connect("127.0.0.1")
    mqttc.subscribe('examen')

    while (True):
        mqttc.loop()
except KeyboardInterrupt:
    print("Exiting program")
    mqttc.loop_stop()
    GPIO.cleanup()


if __name__ == "__main__":
    main()

