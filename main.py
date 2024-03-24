from drivers.axis import *
from drivers.head import Head
from drivers.carousel import Carousel
from functionLib import *
from test_vacuum_pump import *
import time

# Create instances of the objects
x = XAxis()
y = YAxis()
z = ZAxis()
p = Head()
c = Carousel()

def extract(uL: int):
	p.down_uL(p.max_uL) #Empty air from pipette
	z.down(1500) #Lower pipette into vial
	p.up_uL(uL) #Fill pipette with fluid
	time.sleep(0.25)
	z.up(1500) #Raise pipette above vial again
	
def weigh(uL: int):
	extract(uL)
	
	x.right(200)
	z.down(1500)
	
	p.down_uL(uL)
	time.sleep(0.5)
	p.up_uL(p.max_uL)
	
	z.up(1500)
	x.left(200)

def go_to_vial():
	go_to((y,x,z),(3150,435,664),True)

def pipette_to_spincoater():
	go_to((y,x,z),(4400,522,1670),True)

def suction_to_spincoater():
	#yx((z,y,x),(2700,3950,475),True) #good enough coords for suction to spincoater
	go_to((y,x,z),(3751,522,1670),True)

def tip_me():
	'''Gets a tip'''
	go_to((y,x,z),(1285,13,3773),True)

def toss_tip():
	'''Disposes of a tip'''
	go_to((y,x,z),(100,900,3000),True)
	y.go_home()
	z.up(1400)
	time.sleep(0.1)
	z.down(1400)
	y.inward(100)

def retrieve_liquid(uL, vial_num):
    go_to_vial()
    c.move_to_vial(vial_num)
    extract(uL)

def demo():
	tip_me()
	toss_tip()
	home()

def home():
	'''Homes all axes'''
	z.go_home()
	x.go_home()
	y.go_home()

# Executes whatever commands the user inputs
if __name__ == "__main__":
	while(True):
		print("Type 'demo()' to run pipette & z-axis demo")
		cmd = input(">> ")
		try:
			exec(cmd)
		except Exception as E:
			print(f"Error {E}, try again.")
