from drivers.axis import *
from drivers.head import Head
from drivers.carousel import Carousel
from functionLib import zyx
from test_vacuum_pump import *
import time

# Create instances of the objects
x = XAxis()
y = YAxis()
z = ZAxis()
p = Head()
c = Carousel()
	
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

def enter_vial(vial_num: int):
	zyx((z,y,x),(4000,3200,470),False)
	c.move_to_vial(5)
	z.down(2400)


# Executes whatever commands the user inputs
if __name__ == "__main__":
	while(True):
		print("Type 'demo()' to run pipette & z-axis demo")
		cmd = input(">> ")
		try:
			exec(cmd)
		except Exception as E:
			print(f"Error {E}, try again.")
