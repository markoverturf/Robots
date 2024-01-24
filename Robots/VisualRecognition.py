from imageai.Detection import ObjectDetection
import os
import cv2

current_directory = os.getcwd()

camera = cv2.VideoCapture(0)

detector = ObjectDetection()

detector.setModelTypeAsYOLOv3()

detector.setModelPath(current_directory + "\yolov3.pt")
detector.loadModel()
while True:
    ret, frame = camera.read()

    returned_image, detections = detector.detectObjectsFromImage(
    input_image = (frame),
    output_type = "array"
    )
    for eachObject in detections:
        print(
             eachObject["name"] , " : ",
             eachObject["percentage_probability"], " : ",
             eachObject["box_points"] )
        print("--------------------------------")

    cv2.imshow('frame', returned_image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break