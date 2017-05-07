#!/usr/bin/python

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(7, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)

ledCount = 5
currentLed = -1
leds = [7, 11, 13, 15, 16]
sequenceValue = 1
decreaseSeq = 0.2

def setLeds():
    for led in leds:
	GPIO.output(led, False)	   
    GPIO.output(leds[currentLed], True)
    time.sleep(sequenceValue)

def updateLeds():
    global currentLed
    currentLed += 1
    if (currentLed == 5):
	currentLed = 0


def hit(self):
    global sequenceValue
    global decreaseSeq
    if (currentLed == 2):
	sequenceValue -= decreaseSeq
    else:
	sequenceValue = 2
    print(sequenceValue)

GPIO.add_event_detect(19, GPIO.FALLING, callback=hit, bouncetime=300) 

try:
    while (True):
        updateLeds()
        setLeds()
    

except KeyboardInterrupt:
    print("Shutting down program and disabling pins")
    GPIO.cleanup()
