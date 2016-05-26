import RPi.GPIO as gpio
import dht11
import datetime
import time

trig_pin = 13
echo_pin = 19
led_pin = 16

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.setup(trig_pin, gpio.OUT)
gpio.setup(echo_pin, gpio.IN)
gpio.setup(16, gpio.OUT)
gpio.setup(20, gpio.OUT)
gpio.setup(21, gpio.OUT)
#gpio.cleanup()

instance = dht11.DHT11(pin = 6)

try:
	while True:
		gpio.output(trig_pin, False)
		time.sleep(1)
		gpio.output(trig_pin, True)
		time.sleep(0.00001)
		gpio.output(trig_pin, False)

		while gpio.input(echo_pin) == 0:
			pulse_start = time.time()

		while gpio.input(echo_pin) == 1:
			pulse_end = time.time()

		pulse_duration = pulse_end - pulse_start
		distance = pulse_duration * 17000
		distance = round(distance, 2)

		print "Distance : ", distance, "cm"

		result = instance.read()
		if result.is_valid():
			print("Last valid input : " + str(datetime.datetime.now()))
		elif result.temperature == 0:
			result.temperature = 25

		if result.temperature <= 25:
			if distance <= 30:
				gpio.output(led_pin, False)
				led_pin = 16
				gpio.output(led_pin, True)
				print("Temperature : %dC" % result.temperature)
				print "Red LED ON"
			elif distance < 100:
				gpio.output(led_pin, False)
				led_pin = 20
				gpio.output(led_pin, True)
				print("Temperature : %dC" % result.temperature)
				print "Yellow LED ON"
			else:
				gpio.output(led_pin, False)
				led_pin = 21
				gpio.output(led_pin, True)
				print("Temperature : %dC" % result.temperature)
				print "Green LED ON"

		else:
			gpio.output(led_pin, False)
			print("Temperature : %dC" % result.temperature)
			print "temperature is too high"

		print "----------------------------------------"

except KeyboardInterrupt:
	gpio.cleanup()
