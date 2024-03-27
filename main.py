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
s = SpinCoater()
h = HotPlate()

# Functions for Pipette Tip
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

# Functions for Carousel Stage
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

# Functions for Spin Coater Stage
def pipette_to_spincoater(): 
	g.go_to((4400,522,1670),True)

def suction_to_spincoater(): 
	g.go_to((3751,522,1670),True)

def get_slide():
	g.go_to(SLIDE_HOLDER,True)
	p.lower_cup()
	c.vac_on()
	p.raise_cup()
	g.home()

def drop_slide_to_spin():
	pass

def retrieve_slide_from_spin():
	pass

def slide_to_hot():
	pass

def retrieve_slide_from_hot():
	pass

# Actual Procedure Code to be used in GUI
def procedure(solutions: list[tuple[int, int]], steps: list[tuple[int,int]], hot_time: int, antisolvent: tuple[int, int]):
	'''
	solutions: list[(vial_num, percentage_mix)]
	steps: list[(rpm, time)]
	hot_time: bake time in seconds for hot plate
	antisolvent: (dispense_time, volume)

	for now i am going to add a +1 to the vial_num to make them the same as constants
	'''
	if len(solutions) != 3:
		raise ValueError("Must select 3 solutions")
	
	if len(steps) != 3:
		raise ValueError("Must select 3 steps")

	g.home()
	tip_increment = (0,0) #keeping track of tip location
	tip_increment = tip_on(tip_increment)

	# Carousel Stage
	for sol in solutions:
		vial_num, percentage_mix = sol
		vial_num += 1 #correcting gui starting at 0 but maybe correct in gui
		volume = percentage_mix/100 * p.max_uL
		for _ in range(4):
			extract_from_vial(volume, vial_num)
			dispense_in_vial(VIAL_EMPTY_A)
		wash_tip()
	
	g.home() #recalibrate between each stage
	
	# Spin Coater Stage
	s.connect()
	get_slide()
	drop_slide_to_spin() #needs to be written, but drop slide in spin coater
	anti_disp_time, anti_vol = antisolvent #use antisolvent inputs
	extract_from_vial(anti_vol, VIAL_ANTISOLVENT)
	total_spin_time = 0
	for spin_step in steps:
		rpm, spin_time = spin_step
		s.add_step(rpm, spin_time)
		total_spin_time += spin_time
	pipette_to_spincoater()
	start_time = time.perf_counter()
	current_time = 0
	s.run()
	while(current_time < anti_disp_time):
		current_time = time.perf_counter()-start_time
	p.empty()
	time.sleep(total_spin_time - anti_disp_time)
	
	tip_off()
	g.home() #recalibrate between stages again
    
	# Hot Plate Stage
	retrieve_slide_from_spin() #need to write but retrieve slide from spin coater
	slide_to_hot() #need to write but bring slide to hot plate
	h.anneal(hot_time)
	retrieve_slide_from_hot() #maybe???????

# Executes whatever commands the user inputs
if __name__ == "__main__":
	while(True):
		print("Type 'demo()' to run pipette & z-axis demo")
		cmd = input(">> ")
		try:
			exec(cmd)
		except Exception as E:
			print(f"Error {E}, try again.")
