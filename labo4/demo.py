import paho.mqtt.client as mqtt
import json
import RPi.GPIO as io

# tuplje object met pin nummers
leds = (11, 13, 15) 

# initialisatie functie voor leds met als parameter een tuple
def init_leds(leds):
    io.setmode(io.BOARD)
    io.setup(leds, io.OUT)

# set state van de leds met als parameters 2 tuples
# tuple van pin nummers en een met bools van de state
def set_leds(leds, states):
    io.output(leds, states)

# calback voor het verwerken van de berichten
def on_message(mqttc, obj, msg):
    print("Message Received")
    try:
        # payload omzetten van bytestring naar string
        p = msg.payload.decode("utf-8")
        
        # json wordt verwacht json string moet omgezet worden naar een python
        #  dictonary voor verwerking
        x = json.loads(p)

        #
        set_leds(leds, tuple(x['leds']))
        return
    except Exception as e:
        print(e)


def main():
    try:
        # initialisatie van alle elementen
        init_leds(leds)
        mqttc = mqtt.Client()
        mqttc.on_message = on_message
        mqttc.connect("127.0.0.1")
        mqttc.subscribe('tmp')
        while True:
                mqttc.loop()
    except KeyboardInterrupt:
        pass
    finally:
        io.cleanup()

# main segment
if __name__ == "__main__":
    main()
