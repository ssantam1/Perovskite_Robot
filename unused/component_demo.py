'''
File to Demo Components Separately

Created by Pierce Alvir and Steven Santamorena
'''
from main import *
from drivers.axis import *
from drivers.head import Head
from drivers.carousel import Carousel
from drivers.spincoater import SpinCoater
from drivers.hotplate import HotPlate
import time

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

def demo_procedure(solutions: list[tuple[int, int]], steps: list[tuple[int,int]], hot_time: int, antisolvent: tuple[int, int]):
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
	vial_num, percentage_mix = solutions[0]
	vial_num += 1 #correcting gui starting at 0 but maybe correct in gui
	volume = percentage_mix/100 * p.max_uL
	for _ in range(4):
		extract_from_vial(volume, vial_num)
		dispense_in_vial(VIAL_EMPTY_A)
	wash_tip()
	mix_vial(VIAL_EMPTY_A)

	g.home() #recalibrate between each stage
	
	# Spin Coater Stage
	s.connect()
	get_slide()
	drop_slide_to_spin() #needs to be written, but drop slide in spin coater
	extract_from_vial(p.max_uL, VIAL_EMPTY_A)
	g.go_to(PIP_TO_SPIN, True)
	p.empty()
	anti_disp_time, anti_vol = antisolvent #use antisolvent inputs
	extract_from_vial(anti_vol, VIAL_ANTISOLVENT)
	total_spin_time = 0
	for spin_step in steps:
		rpm, spin_time = spin_step
		s.add_step(rpm, spin_time)
		total_spin_time += spin_time
	g.go_to(PIP_TO_SPIN, True)
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