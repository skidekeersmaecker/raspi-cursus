#!/usr/bin/python
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

GPIO.setup(16, GPIO.OUT)
GPIO.setup(15, GPIO.IN)

pwm=GPIO.PWM(16, 1000)
pwm.start(0)

brightness=0

try:
    while (True):
        if (GPIO.input(15)):
	    brightness += 5
	    pwm.ChangeDutyCycle(brightness)
	    time.sleep(0.2)

	if (brightness == 50):
	    brightness = 0

except KeyboardInterrupt:
    print("Program is shutdown and pins are disabled")
    GPIO.cleanup()
