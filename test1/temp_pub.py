import RPi.GPIO as gpio
import dht11
import paho.mqtt.client as mqtt
import random
import time
import datetime

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)

instance = dht11.DHT11(pin = 6)

mqttc = mqtt.Client("python_pub")
mqttc.connect("127.0.0.1", 1883)
#mqttc.connect("218.150.181.117", 1883)
while 1:
	result = instance.read()
	if result.is_valid():
		print("Last valid input : " + str(datetime.datetime.now()))
	elif result.temperature == 0:
		result.temperature = 25
		print("Initial valid values")
	strResult = str(result.temperature)
	mqttc.publish("environment/temperature", strResult)
	mqttc.loop(2)
	print("temperature : " + strResult + "C")
	time.sleep(1)                                   # sleep 2sec and restart

