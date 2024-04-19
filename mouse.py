

from tkinter import *
import serial
import time
import numpy as np 

pos = np.zeros(10)

class Mouse:

    def __init__(self):
        self.posx = np.zeros(50)

    def map_range_x(self, old_value):
        old_min = 0
        new_min = 170 
        old_max = 1280
        new_max = 30
        mapped_value =  int(((old_value - old_min) / (old_max - old_min) ) * (new_max - new_min) + new_min)
        return mapped_value

    def map_range_y(self, old_value):
        old_min = 0
        new_min = 65
        old_max = 720
        new_max = 170
        mapped_value =  int(((old_value - old_min) / (old_max - old_min) ) * (new_max - new_min) + new_min)
        return mapped_value


    def motion(self, event):
        x, y = self.map_range_x(event.x), self.map_range_y(event.y)
        data = '{}x{}y'.format(x,y)
        arduino.write(bytes(data, 'utf-8'))
        time.sleep(0.05)
        ser_data = arduino.readline()
        print(ser_data)
        #print('{}, {}'.format(x, y))


arduino = serial.Serial(port='/dev/ttyACM0', baudrate=500000, timeout=.1)
#/dev/cu.usbserial-410 /dev/cu.usbmodem4101

# create root window
root = Tk()
# root window title and dimension
root.title("mouse")
# Set geometry(widthxheight)
root.geometry('1280x720')

mouse = Mouse()

"""posi = 0
dir = True 
while(True):
    arduino.write(bytes(str(posi), 'utf-8'))
    if posi == 181: dir = False
    if posi == 0: dir = True 
    if dir: posi += 1 
    else: posi -= 1
    time.sleep(0.05)
    data = arduino.readline()
    print(data)
"""
root.bind('<Motion>', mouse.motion)

# Execute Tkinter
root.mainloop()
