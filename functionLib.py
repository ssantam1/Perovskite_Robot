'''

Created by Pierce Alvir and Steven Santamorena

'''
from drivers.axis import *



# Function for pipette tip pick up
def tip_on(incrementer: int) -> int:
    '''
    incrementer: stored variable in main file that knows what iteration to set the tip to
    function returns incrementer number as well
    '''
    y_coord, x_coord, z_coord = PIP_TO_TIP
    
    go_to((y,x,z),(,1308,13),True)

# Function for pipette tip ejection
def tip_off():
	'''
        ejects tip should be same for any time you want to take tip off

        maybe consider washing the tips instead of ejecting
        '''
	go_to((y,x,z),(1000,100,900),True)
	y.go_home()
	z.up(1400)
	z.down(1400)
	y.inward(100)
# Function for antisolvent pick up

# Function for slide pick up
