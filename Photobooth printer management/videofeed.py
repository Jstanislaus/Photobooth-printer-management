#!/usr/bin/python3

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
for time_left in range(10, 0, -1):
    colour = (0, 255, 0, 255)
    origin = (0, 30)
    font = cv2.FONT_HERSHEY_SIMPLEX
    scale = 1
    thickness = 2
    overlay = np.zeros((640, 480, 4), dtype=np.uint8)
    cv2.putText(overlay, str(time_left), origin, font, scale, colour, thickness)
    picam2.set_overlay(overlay)
    i+=1
    time.sleep(1)

picam2.stop()
print(i)