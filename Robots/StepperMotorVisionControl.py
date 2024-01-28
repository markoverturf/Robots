import pyfirmata
import time
import os
import cv2
import threading
import asyncio
from tkinter import *
from IPython.display import clear_output
from types import SimpleNamespace
from imageai.Detection import ObjectDetection
from IPython.display import clear_output

current_directory = os.getcwd()

camera = cv2.VideoCapture(0)
#camera.resize(im, (960, 540))

camera.set(3, 640)
camera.set(4, 480)

detector = ObjectDetection()

detector.setModelTypeAsYOLOv3()

detector.setModelPath(current_directory + "\yolov3.pt")
detector.loadModel()

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
    elif stop==False:
        stop = True

def rest():
    board.digital[int1].write(0)
    board.digital[int2].write(0)
    board.digital[int3].write(0)
    board.digital[int4].write(0)

def CWdirect():
    global direction
    global stop
    direction = "CW"

def CCWdirect():
    global direction
    global stop
    direction = "CCW"

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

#### Initialize Vision System ####
while True:
    ret, frame = camera.read()
    returned_image, detections = detector.detectObjectsFromImage(
    input_image = (frame),
    output_type = "array")
    for eachObject in detections:
        if eachObject["name"] == "person":
            print(
                eachObject["percentage_probability"], " : ",
                eachObject["box_points"])
            x1 = eachObject["box_points"][0]
            y1 = eachObject["box_points"][1]
            x2 = eachObject["box_points"][2]
            y2 = eachObject["box_points"][3]
            centerx = (x2 - x1)/2
            centery = (y2 - y1)/2
            print(centerx)
            print(centery)
            clear_output(wait = True)
            start_point = (int(centerx - 10), int(centery + 10)) 
            end_point = (int(centerx + 10), int(centery - 10))
            color = (0, 0, 255) 
            thickness = -1
            cv2.rectangle(returned_image, start_point, end_point, color, thickness)
            if centerx + 10 >= 310 
                if direction != 'CW':
                    direct = 'CW'
                if stop != False
                    stop = False
            elif centerx - 10 <= 330
                if direction != 'CCW':
                    direction = 'CCW'
                if stop != False
                    stop = False
            else:
                if stop != True
                    stop = True
    cv2.imshow('Image Recognition', returned_image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
        
#### Exit Program ####

rest()