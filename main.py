'''

Procedure Generation File
Created by Pierce Alvir and Steven Santamorena

'''
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

# Function for keeping track and performing xyz movement    
def go_to(axis: tuple[YAxis, XAxis, ZAxis], coord: tuple[int, int, int], obstacle_det: bool):
	'''
	Need to rewrite to have this function have axes already used in it
	'''
	if obstacle_det:
        axis[2].go_home()

    axis_and_coords = [(axis[i], coord[i]) for i in range(len(axis))]

    '''
    (axis[1], coord[1]),
    (axis[2], coord[2]),
    (axis[3], coord[3])

    for (a, c) in axis_and_coords:
        a.positive(c)
        
    '''
        
    for i in range(3):
        if (coord[i] > axis[i].limit or coord[i] < 0):
            print(f"Error") # Pierce we really need a more descriptive error and also maybe throw an exception
            exit()
        elif (coord[i] > axis[i].pos):
            print("Going positive")
            axis_temp = coord[i]-axis[i].pos
            axis[i].positive(axis_temp)
        else:
            print("Going negative")
            axis_temp = axis[i].pos-coord[i]
            axis[i].negative(axis_temp)
    return axis

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

def tip_on():
	'''Gets a tip'''
	go_to((y,x,z),(1285,13,3773),True)

def tip_off():
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
	tip_on()
	toss_off()
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
