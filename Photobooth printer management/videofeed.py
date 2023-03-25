#!/usr/bin/python3

import time

import numpy as np

from picamera2 import Picamera2, Preview
picam2 = Picamera2()
print("Hi")
picam2.configure(picam2.create_preview_configuration())
print("Hi")
picam2.start_preview(Preview.DRM)
print("Hi")
picam2.start()
time.sleep(1)
overlay = np.zeros((300, 400, 4), dtype=np.uint8)
overlay[:150, 200:] = (255, 0, 0, 64)
overlay[150:, :200] = (0, 255, 0, 64)
overlay[150:, 200:] = (0, 0, 255, 64)

picam2.set_overlay(overlay)
time.sleep(2)
