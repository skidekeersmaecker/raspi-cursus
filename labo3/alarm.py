#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import datetime

GPIO.setmode(GPIO.BOARD)

alarmActivated = False
start = 0
end = 0
elapsed = 0

#ultrasoon
TRIG = 11
ECHO = 7
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

#led
led = 13
GPIO.setup(led, GPIO.OUT)
GPIO.output(led, False)

#button
button = 15
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def alarmListen():
    GPIO.output(TRIG, False)
    time.sleep(0.2)
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    #print(distance)
    if (distance <= 10):
	writeLogFile()
	return True
    return False

def activateAlarm():
    alarmActivated = True
    setLed(True)
    
def setLed(on):
    if (on == True):
	GPIO.output(led, True)
	time.sleep(0.5)
	GPIO.output(led, False)
	time.sleep(0.5)
    else:
	GPIO.output(led, False)

def writeLogFile():
    #timeAlarm = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y") + "\n"
    f = open('ActivatedAlarmTimes.log', 'a')
    #f.write(timeAlarm)
    f.write(time.strftime("%d-%m-%y %H:%M:%S \n"))
    f.close
    #print("time of alarm: ", timeAlarm)

def resetAlarm():
    global alarmActivated
    print("alarm reset")
    alarmActivated = False
    setLed(False)

def listenButton(self):
    global start
    global end
    elapsed = 0
    if GPIO.input(button) == 1:
	start = time.time()
    if GPIO.input(button) == 0:
	end = time.time()
	elapsed = end - start
	#print(elapsed)
	if(elapsed >= 5) and (alarmActivated == True):
	    elapsed = 0
	    resetAlarm()


GPIO.add_event_detect(button, GPIO.BOTH, callback=listenButton, bouncetime=300)

try:
   while(True):
	if (alarmActivated == False):
	    alarmActivated = alarmListen()	
        else:
	    activateAlarm()
        
except KeyboardInterrupt:
    print("exiting program")
    GPIO.cleanup()

