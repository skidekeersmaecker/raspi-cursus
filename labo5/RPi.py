import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import time
import signal
GPIO.setmode(GPIO.BOARD)

# GPIO setup
leftLED = 16
rightLED = 18
GPIO.setup(leftLED, GPIO.OUT)
GPIO.setup(rightLED, GPIO.OUT)
TRIG = 15
ECHO = 16
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(TRIG, GPIO.OUT)

# First start: everything off/0
alarm = False
alarmState = False
distance = 0
run = True

def handler_stop_signals(signum, frame):
  global run
  run = False
  GPIO.cleanup()
  mqttc.loop_stop()
  mqttc.disconnect()

def write(data):
  mqttc.publish("home/labo05/01", data, qos=1)

def on_publish(mqttc, userData, mid):
  print("mid: "+str(mid))

def on_connect(mqttc, userData, resCode):
  print("Connection OK. Result code = "+str(resCode))
  mqttc.subscribe("home/labo05/02")

def on_message(mqttc, userdata, msg):
  print("msg: " + str(msg.payload) + " at topic: " + msg.topic + " with QoS: " + str(msg.qos))
  global alarm
  global distance
  global alarmState
  if (msg.payload == 'dist'):
    write(str(getDistance()))
  elif msg.payload == "trig":
    alarm = False
  elif msg.payload == "on":
    alarmState = True
  elif msg.payload == "off":
    alarmState = False
    alarm = False
  else:
    print("error. Unknown input. Use dist|trig|on|off")

def getDistance():
  GPIO.output(TRIG, True)
  time.sleep(0.00001)
  GPIO.output(TRIG, False)
  while GPIO.input(ECHO) == 0:
    startPulse = time.time()
  while GPIO.input(ECHO) == 1:
    endPulse = time.time()
  deltaPulse = endPulse - startPulse
  distance = deltaPulse * 17150
  distance = round(distance, 2)
  print(distance)
  return distance

def alarmOn():
  global alarm
  global alarmState
  if alarmState:
    GPIO.output(rightLED, True)
    if getDistance() < 30.0:
      alarm = True
      write("Triggered!")
    time.sleep(1)
  elif alarmState == False:
    GPIO.output(rightLED, False)    
  if alarm:
    GPIO.output(leftLED, True)
    time.sleep(1)
    GPIO.output(leftLED, False)
  elif alarm == False:
    GPIO.output(leftLED, False)

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
  try:
    while True:
      mqttc.loop()
      alarmOn()    
  except KeyboardInterrupt:
    print("exiting program")
    mqttc.loop_stop()
    mqttc.disconnect()
    GPIO.cleanup()
if __name__ == "__main__":
  main()
