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






screen.fill(pygame.Color("white")) # clear the screen	
img = pygame.image.load('Template/Whitefriars50th/start_camera.jpg') # load the image
img = pygame.image.load('Template/start_camera.jpg') # load the image
img = img.convert()	
#set_demensions(img.get_width(), img.get_height()) # set pixel dimensions based on image	
x = (infoObject.current_w / 2) - (img.get_width() / 2)
y = (infoObject.current_h / 2) - (img.get_height() / 2)
screen.blit(img,(x,y))
pygame.display.flip()


# init global variables from main thread
global Numeral
global Message
global Message2
global Message3
global screen
global background
global pygame
global ImageShowed
global screenPicture
global backgroundPicture
global CountDownPhoto
   
background.fill(pygame.Color("white"))  # White background


background.fill(pygame.Color("black"))
font = pygame.font.Font(None, 100)
text = font.render("test", 1, (227, 157, 200))
textpos = text.get_rect()
textpos.centerx = background.get_rect().centerx
textpos.centery = background.get_rect().centery
        if(ImageShowed):
backgroundPicture.blit(text, textpos)
        else:
background.blit(text, textpos)