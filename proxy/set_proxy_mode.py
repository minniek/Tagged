'''
Set Tagged Proxy modes using GPIO pins

Usage: python3 set_proxy_mode.py

References:
[1] Raspberry Pi 2 GPIO Diagram: http://www.element14.com/community/docs/DOC-73950/l/raspberry-pi-2-model-b-gpio-40-pin-block-pinout
'''

import RPi.GPIO as GPIO
import os, time

GPIO.setmode(GPIO.BOARD) 

'''
Set up button and LED pins for Tagged Proxy mode one: 'a' or 'v'
If mode one is v: add X-Tagged header from client-->server
If mode one is a: do nothing
'''
btn_1 = 11
GPIO.setup(btn_1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
led_1= 13
GPIO.setup(led_1, GPIO.OUT)
GPIO.output(led_1, 0)

'''
Set up button and LED pins for Tagged Proxy mode two 'x'
If mode is x: remove X-Tagged header from server-->client to invalidate server's digital signature
Mode x requires the X-Tagged header to be injected. Therefore, write "vx" to proxy_config file
'''
btn_2 = 19
GPIO.setup(btn_2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
led_2 = 21
GPIO.setup(led_2, GPIO.OUT)
GPIO.output(led_2, 0)

# TODO Replace button with push button or switch, add debouncing if needed
try:
	os.system("echo -n a > proxy_config") # Set default mode
	print("Waiting for input...")
	while True:
		if (GPIO.input(btn_1)):
			print("Tagged Proxy mode one: v")
			os.system("echo -n v > proxy_config")
			GPIO.output(led_1, 1)
		else:
			GPIO.output(led_1, 0)

		if (GPIO.input(btn_2)):
			print("Tagged Proxy mode two: x")
			os.system("echo -n vx > proxy_config")
			GPIO.output(led_2, 1)
		else:
			GPIO.output(led_2, 0)

		#if not (GPIO.input(btn_1)) and (GPIO.input(btn_2)):
			#os.system("echo -n a > proxy_config")
except KeyboardInterrupt:
	GPIO.cleanup() # Clean up all GPIO pins for clean exit
