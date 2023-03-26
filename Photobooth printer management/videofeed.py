from picamera2 import Picamera2, Preview
import time
import cv2
import numpy as np
WIDTH = 1920
HEIGHT = 1080

picam2 = Picamera2()
config = picam2.create_preview_configuration({"size": (1640, 1093)})#{"size": (1280, 960)})
picam2.configure(config)
#1640, 1093
picam2.start_preview(Preview.QTGL, x=0, y=0, width =1640, height =1093)
#previewDRM
picam2.start()
for time_left in range(10, 0, -1):
    colour = (227, 100, 200,255)#(227, 100, 200)
    origin = (0, 0)
    font = cv2.FONT_HERSHEY_DUPLEX#PLAIN
    scale = 15
    thickness = 28
    textsize = cv2.getTextSize(str(time_left), font, scale, thickness)[0]
    textX = int(616 - (textsize[0] / 2))
    textY = int(820 + (textsize[1] / 2))
    #overlay = cv2.imread("1.png", cv2.IMREAD_UNCHANGED)
    #overlay = cv2.resize(overlay,dsize=(20, 50), interpolation=cv2.INTER_CUBIC)
    overlay = np.zeros((1640, 1093, 4), dtype=np.uint8)
    cv2.putText(overlay, str(time_left), (textX, textY ), font, scale, colour, thickness,lineType = cv2.LINE_AA)
    picam2.set_overlay(overlay)
    time.sleep(1)

picam2.stop()
while True:
    pass

