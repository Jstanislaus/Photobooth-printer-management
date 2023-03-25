#!/usr/bin/python3
import time
import cv2
import numpy as np
from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput

#Picamera2.set_logging(Picamera2.DEBUG)
picam2 = Picamera2()
config = picam2.create_video_configuration()
picam2.configure(config)
picam2.start_preview(Preview.DRM, x=0, y=0, width=1920, height=1080)
picam2.start()

def show_texts(rec_time):
    for time_left in range(rec_time, -1, -1):
        colour = (255, 0, 0, 255)
        origin = (0, 50)
        font = cv2.FONT_HERSHEY_SIMPLEX
        scale = 1
        thickness = 2
        overlay = np.zeros((640, 480, 4), dtype=np.uint8)
        cv2.putText(overlay, str(time_left), origin, font, scale, colour, thickness)
        picam2.set_overlay(overlay)
        time.sleep(1)

def record():
    encoder = H264Encoder(1000000)
    timestr = time.strftime("%Y%m%d-%H%M%S")
    encoder.output = FfmpegOutput(timestr+".mp4")
    picam2.start_encoder(encoder)
    show_texts(5)
    picam2.stop_encoder()

record()
time.sleep(1)
record()
time.sleep(1)
record()
time.sleep(1)
record()

picam2.stop()
