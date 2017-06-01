#!/usr/bin/python
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.IN)

ledState = False

try:
    while (True):
        if (GPIO.input(13)):
	    print("pressed")
	    ledState = not ledState
	    GPIO.output(11, ledState)
	    time.sleep(0.2)

except KeyboardInterrupt:
    print("Shutting down program and disabling pins")
    GPIO.cleanup()
