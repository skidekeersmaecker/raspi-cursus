#!/usr/bin/python
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

GPIO.setup(7, GPIO.OUT)
GPIO.setup(19, GPIO.IN)

pwm=GPIO.PWM(7, 1000)
pwm.start(0)

brightness=0

try:
    while (True):
	if (GPIO.input(19)):
	    brightness += 5
	    pwm.ChangeDutyCycle(brightness)
	    time.sleep(0.2)

	if (brightness == 50):
	    GPIO.cleanup()

except KeyboardInterrupt:
    print("Program is shutdown and pins are disabled")
    GPIO.cleanup()
