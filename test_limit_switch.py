import time 
import board
import RPi.GPIO as GPIO

sw_pin = 4

sw_pressed = False
sw_pressed_prev = False

GPIO.setmode(GPIO.BCM)
GPIO.setup(sw_pin, GPIO.IN)

while True:
	sw_pressed = GPIO.input(sw_pin)
	if sw_pressed != sw_pressed_prev:
		if sw_pressed:
			print("Pressed!")
		sw_pressed_prev = sw_pressed
