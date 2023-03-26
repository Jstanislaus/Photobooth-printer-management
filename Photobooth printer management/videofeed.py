from picamera2 import Picamera2, Preview

WIDTH = 1920
HEIGHT = 1080

picam2 = Picamera2()
config = picam2.create_preview_configuration({"size": (WIDTH, HEIGHT)})
picam2.configure(config)

picam2.start_preview(Preview.DRM, x=0, y=0, width=WIDTH, height=HEIGHT)
picam2.start()
