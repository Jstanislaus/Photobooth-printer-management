from picamera2 import Picamera2, Preview
import time
WIDTH = 1920
HEIGHT = 1080

picam2 = Picamera2()
config = picam2.create_preview_configuration({"size": (1280, 1080)})#{"size": (1280, 960)})
picam2.configure(config)

picam2.start_preview(Preview.QTGL, x=0, y=0, width=WIDTH, height=HEIGHT)
#previewDRM
picam2.start()
while True:
    pass

#import cv2
#from pyzbar.pyzbar import decode

#from picamera2 import MappedArray, Picamera2, Preview

#colour = (0, 255, 0)
#font = cv2.FONT_HERSHEY_SIMPLEX
#scale = 1
#thickness = 2



#picam2 = Picamera2()
#picam2.start_preview(Preview.QTGL)
#config = picam2.create_preview_configuration(main={"size": (1280, 960)})
#picam2.configure(config)

#barcodes = []
#picam2.post_callback = draw_barcodes
#picam2.start()
#while True:
#    pass
    #rgb = picam2.capture_array("main")
    #barcodes = decode(rgb)
