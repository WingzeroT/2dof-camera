///+8

import cv2
import numpy as np 
from PIL import Image
import serial
import time

def map_range_x(old_value):
    old_min = 0
    new_min = 170 
    old_max = 1280
    new_max = 30
    mapped_value =  int(((old_value - old_min) / (old_max - old_min) ) * (new_max - new_min) + new_min)
    return mapped_value

def map_range_y(old_value):
    old_min = 0
    new_min = 65
    old_max = 720
    new_max = 170
    mapped_value =  int(((old_value - old_min) / (old_max - old_min) ) * (new_max - new_min) + new_min)
    return mapped_value


arduino = serial.Serial(port='/dev/ttyACM0', baudrate=500000, timeout=.1)

color = [0, 0, 255] # yellow in BGR colorspace 

cap = cv2.VideoCapture(2)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 2)

x, y = 640, 360

while True: 
    ret, frame = cap.read()

    #filtered = cv2.GaussianBlur(frame, (15, 15), 0)
    #filtered_median = cv2.medianBlur(filtered, 25)
    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


    lowerLimit = np.array([0, 165, 28])
    upperLimit = np.array([10, 255, 255])

    mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)
  
    mask_ = Image.fromarray(mask)

    bbox = mask_.getbbox()


    if bbox is not None:
        x1, y1, x2, y2 = bbox
        x = x1 + (x2-x1)/2
        y = y1 + (y2-y1)/2
        frame = cv2.circle(frame, (int(x), int(y)), 10, (255, 50, 0), -1)
        #print(str(x) + " | " + str(y))
        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
        #x, y = map_range_x(x), map_range_y(y)
        data = '{}x{}y'.format(x,y)
        arduino.write(bytes(data, 'utf-8'))
        #time.sleep(0.25)
        ser_data = arduino.readline()
        #print(ser_data)

    #cv2.imshow('frame', mask)
    cv2.imshow('temp', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

