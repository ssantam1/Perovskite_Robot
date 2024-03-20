import board
import RPi.GPIO as GPIO

enable_pin = 7

GPIO.setmode(GPIO.BCM)
GPIO.setup(enable_pin, GPIO.OUT)
GPIO.output(enable_pin, 1)

while True:
	input()
	GPIO.output(enable_pin, 1)
	input()
	GPIO.output(enable_pin, 0)
