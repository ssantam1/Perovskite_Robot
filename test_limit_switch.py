import time 
import board
import RPi.GPIO as GPIO

class LimitSwitch:
	def __init__(self, input_pin: int, debounce_amount: int) -> None:
		self.input_pin = input_pin
		self.debounce_amount = debounce_amount
		self.initialize_switch()
		
		self.state = False

	def initialize_switch(self) -> None:
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.input_pin, GPIO.IN)

	def is_pressed(self) -> bool:
		self.state = GPIO.input(self.input_pin)
		return self.state

if __name__ == "__main__":
	switch = LimitSwitch(4, 10)
	while True:
		if switch.is_pressed():
			print("Switch pressed!")
		else:
			print("Not pressed...")
		time.sleep(0.1)