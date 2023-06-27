#!/usr/bin/python3
import math
import time
import cv2
import time
import numpy as np

from picamera2 import Picamera2, Preview

picam2 = Picamera2()

preview_config = picam2.create_preview_configuration({"size": (1920, 1080)})
picam2.start_preview(Preview.QTGL, x=0, y=0, width=1920, height=1080)
#picam2.create_preview_configuration()
#picam2.start_preview(Preview.QTGL)
picam2.start()
i=0
t_end=time.time()+10
colour = (0, 255, 0, 255)
origin = (0, 30)
font = cv2.FONT_HERSHEY_SIMPLEX
scale = 1
thickness = 2
overlay = np.zeros((640, 480, 4), dtype=np.uint8)
while time.time() < t_end:
    Numeral = str(int(math.floor(t_end-time.time()))+1)
    cv2.putText(overlay, str(Numeral), origin, font, scale, colour, thickness)
    picam2.set_overlay(overlay)
    i+=1

picam2.stop()
print(i)