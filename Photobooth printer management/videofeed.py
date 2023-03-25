#!/usr/bin/python3

import time

picam2 = Picamera2()
picam2.start_preview(True)
picam2.start()
time.sleep(2)
picam2.stop_preview()
time.sleep(2)
picam2.start_preview(True)
time.sleep(2)
picam2.stop()
picam2.stop_preview()
