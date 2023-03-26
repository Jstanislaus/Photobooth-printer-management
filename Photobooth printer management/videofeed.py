from picamera2 import Picamera2, Preview
import time
import cv
import numpy as np
WIDTH = 1920
HEIGHT = 1080

picam2 = Picamera2()
config = picam2.create_preview_configuration({"size": (1640, 1232)})#{"size": (1280, 960)})
picam2.configure(config)

picam2.start_preview(Preview.QTGL, x=0, y=0, width=WIDTH, height=HEIGHT)
#previewDRM
picam2.start()
for time_left in range(10, 0, -1):
    colour = (0, 255, 0, 255)
    origin = (0, 30)
    font = cv2.FONT_HERSHEY_SIMPLEX
    scale = 1
    thickness = 2
    overlay = np.zeros((640, 480, 4), dtype=np.uint8)
    cv2.putText(overlay, str(time_left), origin, font, scale, colour, thickness)
    picam2.set_overlay(overlay)
    time.sleep(1)

picam2.stop()
while True:
    pass

