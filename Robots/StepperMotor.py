import pyfirmata
import time
import os
from tkinter import *
import threading
from IPython.display import clear_output
import asyncio

#### Initialize Variables ####
int1 = 8
int2 = 9
int3 = 10
int4 = 11

pinout1 = 0
pinout2 = 0
pinout3 = 0
pinout4 = 0

step_sleep = 0.1

step_count = 4096 

direction = False

step_sequence = [[1,0,0,1],
                 [1,0,0,0],
                 [1,1,0,0],
                 [0,1,0,0],
                 [0,1,1,0],
                 [0,0,1,0],
                 [0,0,1,1],
                 [0,0,0,1]]

motor_pins = [int1,int2,int3,int4]
motor_step_counter = 0

stop = True

direction = "CW"

#### Define Functions ####

def StartStop():
    global stop
    global StartStop
    if stop==True:
        stop = False
        btnStartStop["text"] = "Stop"
    elif stop==False:
        stop = True
        btnStartStop["text"] = "Start"
        
    '''
    board.digital[int1].write(0)
    board.digital[int2].write(0)
    board.digital[int3].write(0)
    board.digital[int4].write(0)
    '''

def rest():
    global stop
    stop = False

def CWdirect():
    global direction
    global stop
    direction = "CW"
    btnCW.configure(bg="blue")
    btnCCW.configure(bg="gray")

def CCWdirect():
    global direction
    global stop
    direction = "CCW"
    btnCW.configure(bg="gray")
    btnCCW.configure(bg="blue")

def DriveMotor():
    i = 0
    global motor_step_counter
    global step_count
    for i in range(step_count):
        clear_output(wait=True)
        pinout1 = step_sequence[motor_step_counter][0]
        pinout2 = step_sequence[motor_step_counter][1]
        pinout3 = step_sequence[motor_step_counter][2]
        pinout4 = step_sequence[motor_step_counter][3]
        '''
        board.digital[int1].write(step_sequence[motor_step_counter][0])
        board.digital[int2].write(step_sequence[motor_step_counter][1])
        board.digital[int3].write(step_sequence[motor_step_counter][2])
        board.digital[int4].write(step_sequence[motor_step_counter][3])
        '''
        if direction=='CW' and stop==False:
            motor_step_counter = (motor_step_counter - 1) % 8
        elif direction=='CCW' and stop==False:
            motor_step_counter = (motor_step_counter + 1) % 8
        elif stop==True:
            pinout1 = 0
            pinout2 = 0
            pinout3 = 0
            pinout4 = 0
        print(pinout1," ",pinout2," ",pinout3," ",pinout4)
        time.sleep(step_sleep)

def exit():
    stop = True
    pinout1 = 0
    pinout2 = 0
    pinout3 = 0
    pinout4 = 0
    t1.join()
    root.destroy()
    exit(0)
    

#### Start Motor Thread ####

t1 = threading.Thread(target=DriveMotor)
t1.start()

#### Load Tkinter Form ####

root = Tk()
frame = Frame(root)

root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
frame.grid(row=0, column=0, sticky="news")
grid = Frame(frame)
grid.grid(sticky="news", column=0, row=7, columnspan=2)
frame.rowconfigure(7, weight=1)
frame.columnconfigure(0, weight=1)

btnCW = Button(frame, text = "CW", command = CWdirect)
btnCW.grid(column=0, row=0, sticky="news")

btnCCW = Button(frame, text = "CCW", command = CCWdirect)
btnCCW.grid(column=1, row=0, sticky="news")

btnStartStop = Button(frame, text = "Start", command = StartStop)
btnStartStop.grid(row=2, columnspan = 2, sticky="news")

btnStartStop = Button(frame, text = "Exit", command = exit)
btnStartStop.grid(row=3, columnspan = 2, sticky="news")

frame.columnconfigure(tuple(range(2)), weight=1)
frame.rowconfigure(tuple(range(1)), weight=1)

btnCW.configure(bg="blue")
btnCCW.configure(bg="gray")

root.mainloop()

#### Exit Program ####

rest()
exit(0)