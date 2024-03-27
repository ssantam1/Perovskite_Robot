'''
File to Demo Components Separately

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
s = SpinCoater()
h = HotPlate()

# Demo GUI
def gui_demo(solutions: list[tuple[int, int]], steps: list[tuple[int,int]], hot_time: int, antisolvent: tuple[int, int]):
	print(solutions)
	print(steps)
	print(hot_time)
	print(antisolvent)

# Demo Carousel Stage
def carousel_demo(volume, vial_num): 
	tip_on() 
	extract_from_vial(volume,vial_num) #we get the uL from GUI but we need a vial dictionary for each labeled vial whatever GUI asks for
	tip_off()
	g.home()
	
# Demo Spin Coater Stage
def spin_demo(step: tuple[int,int]):
    rpm, spin_time = step
    s.connect()
    s.add(rpm, spin_time)
    s.run()

# Demo Hot Plate Stage
def hot_demo(bake_time: int):
	h.anneal(bake_time)
	
# Important Helper Functions
def tip_on(increments: tuple[int, int]) -> int:
    '''
    must work on this to use incrementer variable and go through multiple tips
    incrementer: stored variable in main file that knows what iteration to set the tip to
    function returns incrementer number as well
    '''
    increment_x, increment_y = increments
    y_coord, x_coord, z_coord = PIP_TO_TIP
    x_offset = 46
    y_offset = 46 * Y_MICROSTEP # multiplied for microstepping test
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
	g.go_to(DISPOSE_BIN,True) #need this for washing stage
	y.go_home()
	z.up(700)
	time.sleep(0.1)
	z.down(700)
	y.inward(100)

def wash_tip():
	extract_from_vial(p.max_uL, VIAL_CLEANER) #4 would be the constant for the cleaning solution in this case
	g.go_to(DISPOSE_BIN,True)
	p.empty()
	g.home()
	
def go_to_vial(): 
	g.go_to(PIP_TO_VIAL,True)

def extract(uL: int): #put in pipette head?
	p.down_uL(p.max_uL) #Empty air from pipette
	z.down(1600) #Lower pipette into vial
	p.up_uL(uL) #Fill pipette with fluid
	time.sleep(0.25)
	z.up(1600) #Raise pipette above vial again

def extract_from_vial(uL, vial_num):
    go_to_vial()
    c.move_to_vial(vial_num)
    extract(uL)

def dispense_in_vial(vial_num):
	go_to_vial()
	c.move_to_vial(vial_num)
	p.empty()

# Executes whatever commands the user inputs
if __name__ == "__main__":
	while(True):
		print("Type 'demo()' to run pipette & z-axis demo")
		cmd = input(">> ")
		try:
			exec(cmd)
		except Exception as E:
			print(f"Error {E}, try again.")