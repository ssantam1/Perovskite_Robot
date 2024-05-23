import board
import RPi.GPIO as GPIO

enable_pin = 25

GPIO.setmode(GPIO.BCM)
GPIO.setup(enable_pin, GPIO.OUT)

def suck() -> None:
	GPIO.output(enable_pin, 1)
	
def blow() -> None:
	GPIO.output(enable_pin, 0)

if __name__ == "__main__":
	while True:
		input()
		GPIO.output(enable_pin, 1)
		input()
		GPIO.output(enable_pin, 0)
