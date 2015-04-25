'''
Set Tagged Proxy modes using Raspberry Pi 2 GPIO pins

Usage: python3 set_proxy_mode.py

References:
[1] Raspberry Pi 2 GPIO Diagram: http://www.element14.com/community/docs/DOC-73950/l/raspberry-pi-2-model-b-gpio-40-pin-block-pinout
'''

import RPi.GPIO as GPIO
import os, time

GPIO.setmode(GPIO.BOARD) 

'''
Set up button and LED pins for Tagged Proxy mode "v"
If mode one is v: inject X-Tagged header from client-->server
'''
btn_1 = 11
GPIO.setup(btn_1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
led_1= 13
GPIO.setup(led_1, GPIO.OUT)
GPIO.output(led_1, 0)

'''
Set up button and LED pins for Tagged Proxy mode "x"
If mode is x: remove X-Tagged header from server-->client to invalidate server's digital signature
Mode x requires the X-Tagged header to be injected. Therefore, write "vx" to proxy_config file
'''
btn_2 = 19
GPIO.setup(btn_2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
led_2 = 21
GPIO.setup(led_2, GPIO.OUT)
GPIO.output(led_2, 0)

'''
Set up button and LED pins for Tagged Proxy default mode "a"
If mode is a: no header injection
'''
btn_3 = 29
GPIO.setup(btn_3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
led_3 = 31
GPIO.setup(led_3, GPIO.OUT)
GPIO.output(led_3, 0)

try:
	os.system("echo a > proxy_config") # Set default mode
	print("Waiting for input...")
	while True:
		if (GPIO.input(btn_1)):
			print("Tagged Proxy in mode v")
			os.system("echo v > proxy_config")
			GPIO.output(led_1, 1)
		else:
			GPIO.output(led_1, 0)

		if (GPIO.input(btn_2)):
			print("Tagged Proxy mode x")
			os.system("echo vx > proxy_config")
			GPIO.output(led_2, 1)
		else:
			GPIO.output(led_2, 0)
			
		if (GPIO.input(btn_3)):
                        print("Tagged Proxy in mode a")
                        os.system("echo a > proxy_config")
                        GPIO.output(led_3, 1)
		else:
			GPIO.output(led_3, 0)
except KeyboardInterrupt:
	GPIO.cleanup() # Clean up all GPIO pins for clean exit
