import pyfirmata
import time
import os
import keyboard

int1 = 8
int2 = 9
int3 = 10
int4 = 11

# careful lowering this, at some point you run into the mechanical limitation of how quick your motor can move
step_sleep = 0.002

step_count = 4096 # 5.625*(1/64) per step, 4096 steps is 360°

direction = False # True for clockwise, False for counter-clockwise

# defining stepper motor sequence (found in documentation http://www.4tronix.co.uk/arduino/Stepper-Motors.php)
step_sequence = [[1,0,0,1],
                 [1,0,0,0],
                 [1,1,0,0],
                 [0,1,0,0],
                 [0,1,1,0],
                 [0,0,1,0],
                 [0,0,1,1],
                 [0,0,0,1]]

motor_pins = [in8,in9,in10,in11]
motor_step_counter = 0 ;

def rest():
    board.digital[int1].write(0)
    board.digital[int2].write(0)
    board.digital[int3].write(0)
    board.digital[int4].write(0)

# the meat
try:
    i = 0
    for i in range(step_count):
        board.digital[int1].write(step_sequence[motor_step_counter][0])
        board.digital[int2].write(step_sequence[motor_step_counter][1])
        board.digital[int3].write(step_sequence[motor_step_counter][2])
        board.digital[int4].write(step_sequence[motor_step_counter][3])
        if direction==True:
            motor_step_counter = (motor_step_counter - 1) % 8
        elif direction==False:
            motor_step_counter = (motor_step_counter + 1) % 8
        else: # defensive programming
            print( "Something went wrong." )
            rest()
            exit(1)
        time.sleep(step_sleep)

except KeyboardInterrupt:
    rest()
    exit(1)

rest()
exit(0)