#!/usr/bin/python

import paho.mqtt.client as mqtt
import time
import signal
import datetime
import RPi.GPIO as GPIO
from slackclient import SlackClient

alarmActiveLed = 16
alarmTriggeredLed = 18
toggleAlarmStateButton = 11
shutdownAlarmButton = 13
distanceButton = 15

GPIO.setmode(GPIO.BOARD)
GPIO.setup(alarmActiveLed, GPIO.OUT)
GPIO.setup(alarmTriggeredLed, GPIO.OUT)
GPIO.setup(toggleAlarmStateButton, GPIO.IN)
GPIO.setup(shutdownAlarmButton, GPIO.IN) 
GPIO.setup(distanceButton, GPIO.IN)

alarmActive = False
alarmTriggered = False
run = True

token = 'token'

def postOnSlack():
    sc = SlackClient(token)
    resp = sc.api_call(
        "chat.postMessage",
        channel="@ski",
        text="Alarm triggered " + time.strftime("%d-%m-%y %H:%M:%S \n")
    )

def writeLogFile():
    f = open('ActivatedAlarmTimes.log', 'a')
    f.write(time.strftime("%d-%m-%y %H:%M:%S \n"))
    f.close

def write(data): 
    global client
    client.publish("home/labo05/02", data, qos = 1)

def on_connect(client, userdata, msg):
    client.subscribe("home/labo05/01")

def on_publish(client, userdata, mid):
    pass

def on_message(client, userdata, msg):
    global alarmTriggered
    if(msg.payload == 'trig'):
        alarmTriggered = True
        postOnSlack()
        writeLogFile()

def TurnOffAlarm(channel):
    global alarmTriggered
    global startTime
    with open('/proc/uptime', 'r') as f:
        currentTime = float(f.readline().split()[0])

    if(GPIO.input(shutdownAlarmButton)):
        startTime = uptime_seconds
    else:
        if((currentTime - startTime) >= 5.0):
            alarm = False
            write("trig")

def ToggleAlarmState(channel):
    global alarmActive
    global alarmTriggered

    alarmActive = not alarmActive

    if(alarmActive == False):
        alarmTriggered = False
    if(alarmActive):
        write('on')
    else:
        write('of')

def AskDistance(channel):
    write('dist')

def handler_stop_signals(signum, frame):
    global run
    run = False

def setLedTriggered(trig):
    if (trig == True):
        GPIO.output(alarmTriggeredLed, True)
        time.sleep(0.5)
        GPIO.output(alarmTriggeredLed, False)
        time.sleep(0.5)
    else:
        GPIO.output(alarmTriggeredLed, False)

def setLedAlarm(on):
    if(on):
        GPIO.output(alarmActiveLed, True)
    else:
        GPIO.output(alarmActiveLed, False)  

GPIO.add_event_detect(toggleAlarmStateButton, GPIO.RISING, callback=ToggleAlarmState, bouncetime=500)
GPIO.add_event_detect(distanceButton, GPIO.RISING, callback=AskDistance, bouncetime=500)
GPIO.add_event_detect(shutdownAlarmButton, GPIO.BOTH, callback=TurnOffAlarm, bouncetime=500)
signal.signal(signal.SIGINT, handler_stop_signals)
signal.signal(signal.SIGTERM, handler_stop_signals)

mqttc = mqtt.Client()
mqttc.on_publish = on_publish
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.username_pw_set("bxaxrkah", "1zQixURXUYuB")
mqttc.connect("m10.cloudmqtt.com", 13915)
mqttc.loop()

def main():
    global mqttc
    global alarmActive
    global alarmTriggered

    try:
        while(True):
            mqttc.loop()
            setLedAlarm(alarmActive)
            setLedTriggered(alarmTriggered)
            
    except KeyboardInterrupt:
        print("exiting program")
        mqttc.loop_stop()
        mqttc.disconnect()
        GPIO.cleanup()

while run:
    if __name__ == "__main__":
        main()
