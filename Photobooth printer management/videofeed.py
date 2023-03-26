import cv2
import numpy as np
import time

from picamera2 import Picamera2

WIDTH = 1920
HEIGHT = 1200

picam2 = Picamera2()
config = picam2.create_preview_configuration({"size": (WIDTH, HEIGHT)})
picam2.configure(config)

picam2.start_preview(Preview.DRM, x=0, y=0, width=WIDTH, height=HEIGHT)
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
