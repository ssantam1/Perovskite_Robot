'''

Procedure Generation File
Created by Pierce Alvir and Steven Santamorena

'''
from drivers.axis import *
from drivers.head import Head
from drivers.carousel import Carousel
from drivers.spincoater import SpinCoater
from drivers.hotplate import HotPlate
import time

# Create instances of the objects 
#maybe rename these from single letters at some point
x = XAxis()
y = YAxis()
z = ZAxis()
g = Gantry(y,x,z)
p = Head()
c = Carousel()
#s = SpinCoater()
h = HotPlate()

# Functions to either get rid of or move
def extract(uL: int): #put in pipette head?
	p.down_uL(p.max_uL) #Empty air from pipette
	z.down(1600) #Lower pipette into vial
	p.up_uL(uL) #Fill pipette with fluid
	time.sleep(0.25)
	z.up(1600) #Raise pipette above vial again

def dispense(uL: int):
	p.down_uL(uL)
	time.sleep(0.5)
	p.up_uL(p.max_uL)

# Functions for Pipette Tip
def tip_on(increments: tuple[int, int]) -> int:
    '''
    must work on this to use incrementer variable and go through multiple tips
    incrementer: stored variable in main file that knows what iteration to set the tip to
    function returns incrementer number as well
    '''
    increment_x, increment_y = increments
    y_coord, x_coord, z_coord = PIP_TO_TIP
    x_offset = 5
    y_offset = 5
    y_coord = y_coord + y_offset*increment_y
    x_coord = x_coord + x_offset*increment_x
    g.go_to((y_coord,x_coord,z_coord),True)
    
    if (increment_x > 11):
        increment_x = 0
        increment_y += 1
    else:
        increment_x += 1
		
    return increment_x, increment_y
    

def tip_off():
	'''Disposes of a tip'''
	g.go_to((100,900,2500),True)
	y.go_home()
	z.up(900)
	time.sleep(0.1)
	z.down(900)
	y.inward(100)

# Functions for Carousel Stage
def go_to_vial(): 
	g.go_to((3150,450,664),True)

def extract_vial(uL, vial_num):
    go_to_vial()
    c.move_to_vial(vial_num)
    extract(uL)

def dispense_vial(uL, vial_num):
	go_to_vial()
	c.move_to_vial(vial_num)
	dispense(uL)

def carousel_stage(): #this is a carousel stage basically
	tip_on() 
	retrieve_liquid(100,2) #we get the uL from GUI but we need a vial dictionary for each labeled vial whatever GUI asks for
	tip_off()
	g.home()

# Functions for Spin Coater Stage
def pipette_to_spincoater(): 
	g.go_to((4400,522,1670),True)

def suction_to_spincoater(): 
	g.go_to((3751,522,1670),True)

def slide_pickup():
	pass

def slide_dropoff():
	pass

def demo_spincoater_connection(): #one of our requirements
	s.add_step(1000,20)
	s.run()

def spincoater_stage():
	slide_pickup() #go pick up slide
	slide_dropoff() #put slide in spin coater
	s.add_step(1000,20) #add all steps early on
	#put liquid on slide
	#pick up antisolvent
	#put pipette above slide on spincoater
	#start an antisolvent timer function to dispense at correct time
	s.run() #start run with antisolvent timer 
	#pick up slide when done

# Tip on and off demo
def demo():
	tip_on()
	tip_off()
	g.home()


# Executes whatever commands the user inputs
if __name__ == "__main__":
	while(True):
		print("Type 'demo()' to run pipette & z-axis demo")
		cmd = input(">> ")
		try:
			exec(cmd)
		except Exception as E:
			print(f"Error {E}, try again.")
