# 2019 07 08 : this works
import sys
import pygame
import pygame.camera

pygame.init()
pygame.camera.init()

#create fullscreen display 640x480
xRes = 640
yRes = 480
screen = pygame.display.set_mode((xRes,yRes),0)

#find, open and start low-res camera
CameraModel = pygame.camera.list_cameras()
webcam = pygame.camera.Camera(CameraModel[0],(xRes,yRes))
webcam.start()

while True:
    #grab image, scale and blit to screen
    imagen = webcam.get_image()
    imagen = pygame.transform.scale(imagen,(xRes,yRes))
    screen.blit(imagen,(0,0))

    #draw all updates to display
    pygame.display.update()

    # check for quit events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            webcam.stop()
            pygame.quit()
            sys.exit()