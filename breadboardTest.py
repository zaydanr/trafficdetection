import RPi.GPIO as GPIO
import time
import random 
from paho.mqtt import client as mqtt_client
import json

redLedPin = 17
greenLedPin = 21
yellowLedPin = 20

DEVICE = 0x76 # Default device I2C address
broker = 'mqtt.things.ph' #INPUT BROKER NAME
port = 1883
topic = "TrafficLightPi" #INPUT TOPIC NAME
client_id = f'publish-{random.randint(0, 1000)}'
username = '65ccc2a11a0ee012cb43b23b' #INPUT USERNAME
password = '9kHQ7THcvfAxEEQNr24BVQy1' #INPUT PASSWORD

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client
    
def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        
        if(msg.payload.decode() == 'green_on'):
            print("Turning green light ON")
            GPIO.output(greenLedPin, GPIO.HIGH)
            msg = {
            "hardware_serial": "TrafficLightPi",
            "payload_fields": {
                "green_light": 1
                }
                }
            result = client.publish(topic, payload=json.dumps(msg),qos=0,retain=False)
            status = result[0]
            if status == 0:
               print(f"Send `{msg}` to topic `{topic}`")
            else:
               print(f"Failed to send message to topic {topic}")
               
        elif(msg.payload.decode() == "green_off"):
            print("Turning green light OFF")
            GPIO.output(greenLedPin, GPIO.LOW)
            msg = {
            "hardware_serial": "TrafficLightPi",
            "payload_fields": {
                "green_light": 0
                }
                }
            result = client.publish(topic, payload=json.dumps(msg),qos=0,retain=False)
            status = result[0]
            if status == 0:
               print(f"Send `{msg}` to topic `{topic}`")
            else:
               print(f"Failed to send message to topic {topic}")
               
        elif(msg.payload.decode() == "yellow_on"):
            print("Turning yellow light ON")
            GPIO.output(yellowLedPin, GPIO.HIGH)
            msg = {
            "hardware_serial": "TrafficLightPi",
            "payload_fields": {
                "yellow_light": 1
                }
                }
            result = client.publish(topic, payload=json.dumps(msg),qos=0,retain=False)
            status = result[0]
            if status == 0:
               print(f"Send `{msg}` to topic `{topic}`")
            else:
               print(f"Failed to send message to topic {topic}")
               
        elif(msg.payload.decode() == "yellow_off"):
            print("Turning yellow light OFF")
            GPIO.output(yellowLedPin, GPIO.LOW)
            msg = {
            "hardware_serial": "TrafficLightPi",
            "payload_fields": {
                "yellow_light": 0
                }
                }
            result = client.publish(topic, payload=json.dumps(msg),qos=0,retain=False)
            status = result[0]
            if status == 0:
               print(f"Send `{msg}` to topic `{topic}`")
            else:
               print(f"Failed to send message to topic {topic}")
               
        elif(msg.payload.decode() == "red_on"):
            print("Turning red light ON")
            GPIO.output(redLedPin, GPIO.HIGH)
            msg = {
            "hardware_serial": "TrafficLightPi",
            "payload_fields": {
                "red_light": 1
                }
                }
            result = client.publish(topic, payload=json.dumps(msg),qos=0,retain=False)
            status = result[0]
            if status == 0:
               print(f"Send `{msg}` to topic `{topic}`")
            else:
               print(f"Failed to send message to topic {topic}")

        elif(msg.payload.decode() == "red_off"):
            print("Turning red light OFF")
            GPIO.output(redLedPin, GPIO.LOW)
            msg = {
            "hardware_serial": "TrafficLightPi",
            "payload_fields": {
                "red_light": 0
                }
                }
            result = client.publish(topic, payload=json.dumps(msg),qos=0,retain=False)
            status = result[0]
            if status == 0:
               print(f"Send `{msg}` to topic `{topic}`")
            else:
               print(f"Failed to send message to topic {topic}")
                           
    client.subscribe(topic)
    client.on_message = on_message
    
def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(redLedPin, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(greenLedPin, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(yellowLedPin, GPIO.OUT, initial=GPIO.LOW)



def run():
   client = connect_mqtt()
   subscribe(client)
   client.loop_forever()

def destroy():
   GPIO.output(redLedPin, GPIO.LOW)
   GPIO.output(yellowLedPin, GPIO.LOW)
   GPIO.output(greenLedPin, GPIO.LOW)
   GPIO.cleanup()                     # Release resource

if __name__ == '__main__':     # Program start from here
   setup()
   try:
      run()
   except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
      destroy()
