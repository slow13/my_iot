import RPi.GPIO as gpio
import dht11
import time
import datetime

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
#gpio.cleanup()

instance = dht11.DHT11(pin=5)
try:
	while True:
		result = instance.read()
		if result.is_valid():
			print("Last valid input : " + str(datetime.datetime.now()))
			print("Temperature : %dC" % result.temperature)
			print("Humidity : %d %%" % result.humidity)
#		else: print("Valid Error")
		time.sleep(1)

except KeyboardInterrupt:
	gpio.cleanup()
