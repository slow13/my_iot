import RPi.GPIO as gpio
import paho.mqtt.client as mqtt
import time

ultra = 0                        # create global variable 
temp = 0
level = ""

led_pin = 16

gpio.setmode(gpio.BCM)
gpio.setup(16, gpio.OUT)
gpio.setup(20, gpio.OUT)
gpio.setup(21, gpio.OUT)

def on_connect(client, userdata, rc):
	gpio.output(16, False)
	gpio.output(20, False)
	gpio.output(21, False)
	print("Connected with result code " + str(rc))
	client.subscribe("environment/#")
	
def on_message(client, userdata, msg):
	global temp, ultra, led_pin
	if msg.topic == "environment/ultrasonic":         # classify messages based on the topic
		ultra = float(msg.payload)
	elif msg.topic == "environment/temperature":
		temp = float(msg.payload)
		
	if temp <= 25:
		if ultra <= 30:                                # classify level based on the discomfort index
			gpio.output(led_pin, False)
			led_pin = 16
			gpio.output(led_pin, True)
			level = "Red LED ON"
		elif ultra <= 100:
			gpio.output(led_pin, False)
			led_pin = 20
			gpio.output(led_pin, True)
			level = "Yellow LED ON"
		else:
			gpio.output(led_pin, False)
			led_pin = 21
			gpio.output(led_pin, True)
			level = "Green LED ON"
	else:
		gpio.output(led_pin, False)
		level = "Temperature is too high"

	print("Temperature : " + str(temp) + "C" + "  Distance : " + str(ultra) + "cm")   # print temperature and ultrasonic
	print(level)               # print level

client = mqtt.Client("pub client")
client.on_connect = on_connect
client.on_message = on_message

client.connect("127.0.0.1", 1883, 60)

#client.loop_start()
client.loop_forever()
	


		

