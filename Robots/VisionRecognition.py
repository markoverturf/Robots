from imageai.Detection import ObjectDetection
import os
import cv2
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
    cv2.imshow('Image Recognition', returned_image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break