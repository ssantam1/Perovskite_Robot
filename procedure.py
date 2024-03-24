from drivers.axis import *
from drivers.head import Head
from drivers.carousel import Carousel
from functionLib import zyx
import time

#Create tuple constants for XYZ coords for things
#PICK_UP_COORDS = (x,y,z)
#Create instances of the objects
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
	#zyx((z,y,x),(4000,3165,470),False)
	c.move_to_vial(vial_num)
	zyx((z,y,x),(1600,3165,470),True) #coordinate for vial make this into tuple please

def pipette_to_spincoater():
	zyx((z,y,x),(2700,4400,525),True) #good enough coords for pipette to spincoater

def suction_to_spincoater():
	zyx((z,y,x),(2700,3950,475),True) #good enough coords for suction to spincoater

def tip_me():
	'''Gets a tip'''
	zyx((z,y,x),(300,1308,13),True)

def toss_tip():
	'''Disposes of a tip'''
	zyx((z,y,x),(1000,100,900),True)
	y.go_home()
	z.up(1400)
	z.down(1400)
	y.inward(100)
	
def retrieve_liquid(uL, vial_num):
    zyx((z,y,x), (3400,3165,470), True)
    c.move_to_vial(vial_num)
    p.down_uL(p.max_uL)
    z.down(1800)
    p.up_uL(uL)
    time.sleep(0.25)
    zyx((z,y,x), (3400,3165,470), True)
    
def home():
	'''Homes all axes'''
	if not z.is_home():
		zyx((z,y,x),(z.limit, y.pos, x.pos),True)
	x.go_home()
	y.go_home()
	z.go_home()
	
def main():
    tip_me()
    retrieve_liquid(100,5)
    toss_tip()
    y.inward(200)
    home()
    
def command_line():
    while True:
        print("Type 'demo()' to run pipette & z-axis demo")
        cmd = input(">> ")
        try:
            exec(cmd)
        except Exception as E:
            print(f"Error {E}, try again.")


# Executes whatever commands the user inputs
if __name__ == "__main__":
    command_line()

'''
help for time stuff
start = time.perf_counter()
end = time.perf_counter()
'''
