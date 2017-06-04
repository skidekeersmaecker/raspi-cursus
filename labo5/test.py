import RPi.GPIO as GPIO
import time

def main():
    global client
    global alarmActive
    global alarmTriggered

    try:
        while(True):
            #mqttc.loop()
            #setLedAlarm(alarmActive)
            #setLedTriggered(alarmTriggered)
            print('True')
            time.sleep(1)
    except KeyboardInterrupt:
        print("exiting program")
        #mqttc.loop_stop()
        #mqttc.disconnect()
        GPIO.cleanup()

if __name__ == "__main__":
    main()

