import pyfirmata
import time
import os
from tkinter import *
import threading
from IPython.display import clear_output
import asyncio
from types import SimpleNamespace

board = pyfirmata.Arduino('COM5')

#### Initialize Variables ####
int1 = 8
int2 = 9
int3 = 10
int4 = 11

p1 = 0
p2 = 0
p3 = 0
p4 = 0

step_sleep = 0.001

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

def rest():
    board.digital[int1].write(0)
    board.digital[int2].write(0)
    board.digital[int3].write(0)
    board.digital[int4].write(0)

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
    global p1, p2, p3, p4
    for i in range(step_count):
        clear_output(wait=True)
        if stop_event.is_set():
            break
        if stop==True:
            rest()
        elif stop==False:
            p1 = step_sequence[motor_step_counter][0]
            p2 = step_sequence[motor_step_counter][1]
            p3 = step_sequence[motor_step_counter][2]
            p4 = step_sequence[motor_step_counter][3]
            board.digital[int1].write(p1)
            board.digital[int2].write(p2)
            board.digital[int3].write(p3)
            board.digital[int4].write(p4)
            if direction=='CW':
                motor_step_counter = (motor_step_counter - 1) % 8
            elif direction=='CCW':
                motor_step_counter = (motor_step_counter + 1) % 8
        print(p1," ",p2," ",p3," ",p4)
        time.sleep(step_sleep)

def exit():
    rest()
    board.digital[int1].write(0)
    board.digital[int2].write(0)
    board.digital[int3].write(0)
    board.digital[int4].write(0)
    stop_event.set()
    root.destroy()

#### Start Motor Thread ####
stop_event = threading.Event()
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

btnExit = Button(frame, text = "Exit", command = exit)
btnExit.grid(row=3, columnspan = 2, sticky="news")

frame.columnconfigure(tuple(range(2)), weight=1)
frame.rowconfigure(tuple(range(1)), weight=1)

btnCW.configure(bg="blue")
btnCCW.configure(bg="gray")

root.mainloop()

#### Exit Program ####

rest()