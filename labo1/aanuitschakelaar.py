#!/usr/bin/python
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

GPIO.setup(7, GPIO.OUT)
GPIO.setup(19, GPIO.IN)

ledState = False

try:
    while (True):
        if (GPIO.input(19)):
	    ledState = not ledState
	    GPIO.output(7, ledState)
	    time.sleep(0.2)

except KeyboardInterrupt:
    print("Shutting down program and disabling pins")
    GPIO.cleanup()
