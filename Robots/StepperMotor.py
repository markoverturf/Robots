import pyfirmata
import time
import os
import keyboard

os.system("pip3 install keyboard")

board = pyfirmata.Arduino('COM3')
while True:
    if keyboard.is_pressed('space'):
        board.digital[13].write(1)
        time.sleep(0.1)
    else:
        board.digital[13].write(0)
        time.sleep(0.1)

in8 = 8
in9 = 9
in10 = 10
in11 = 11

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
    board.digital[in8].write(0)
    board.digital[in9].write(0)
    board.digital[in10].write(0)
    board.digital[in11].write(0)

# the meat
try:
    i = 0
    for i in range(step_count):
        for pin in range(0, len(motor_pins)):
            GPIO.output( motor_pins[pin], step_sequence[motor_step_counter][pin] )
        if direction==True:
            motor_step_counter = (motor_step_counter - 1) % 8
        elif direction==False:
            motor_step_counter = (motor_step_counter + 1) % 8
        else: # defensive programming
            print( "uh oh... direction should *always* be either True or False" )
            cleanup()
            exit( 1 )
        time.sleep( step_sleep )

except KeyboardInterrupt:
    cleanup()
    exit( 1 )

cleanup()
exit( 0 )
