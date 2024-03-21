from drivers.xaxis import Xaxis
from drivers.yaxis import Yaxis
from drivers.zaxis import Zaxis
from drivers.head import Head
from test_vacuum_pump import *
import time

# Create instances of the objects
x = Xaxis()
y = Yaxis()
z = Zaxis()
p = Head()
	
def weigh(uL: int):
	p.down_uL(p.max_uL) #Empty air from pipette
	z.down(1500) #Lower pipette into vial
	p.up_uL(uL) #Fill pipette with fluid
	time.sleep(0.25)
	z.up(1500) #Raise pipette above vial again
	
	x.right(200)
	z.down(1500)
	
	p.down_uL(uL)
	time.sleep(0.5)
	p.up_uL(p.max_uL)
	
	z.up(1500)
	x.left(200)

# Executes whatever commands the user inputs
if __name__ == "__main__":
	while(True):
		print("Type 'demo()' to run pipette & z-axis demo")
		cmd = input(">> ")
		try:
			exec(cmd)
		except Exception as E:
			print(f"Error {E}, try again.")
