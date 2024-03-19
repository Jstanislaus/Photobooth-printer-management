import pifaceio, time
import pygame

pf = pifaceio.PiFace()


global pygame
NotEvent = True
while NotEvent:
        pf.write(pf.read())
        print(str(pf.read_pin(0)))

        time.sleep(0.2)

#
#while True:
#    pf.write(pf.read())
#    time.sleep(.01)