import pygame
import time
import os
import PIL.Image
import config
import cups
import pifacedigitalio
import qrcode
import datetime
import pygame.camera
from pygame.locals import *
import math
from threading import Thread
from pygame.locals import *
from time import sleep
from PIL import Image, ImageDraw

import RPi.GPIO as GPIO, time, os, subprocess,shlex
Venue,portrait,Finalimagereduction,Finalimagereduction2,photos_per_cart,button_pin,IMAGE_WIDTH,IMAGE_HEIGHT = config.config()
#Venue = "AI_2023_05_06_KINGSCORONATIONWHITEFRIARS"
Venueid = Venue[0:2]
Numeral = ""  # Numeral is the number display
Message = ""  # Message is a fullscreen message
Message2 = ""  # Message is a fullscreen message
Message3 = ""
BackgroundColor = ""
CountDownPhoto = ""
CountPhotoOnCart = "" 
#portrait = False
#Finalimagereduction = 5
#Finalimagereduction2 = 70
SmallMessage = ""  # SmallMessage is a lower banner message
TotalImageCount = 0  # Counter for Display and to monitor paper usage
#PhotosPerCart = 3000  # Selphy takes 16 sheets per tray
imagecounter = 0
imagefolder = f"/home/pi/Photobooth_Photos/{Venue}"  #os.path.realpath("../Photos")
templatePath = os.path.join('Template', Venue,"template.png") #Path of template image
start_cameraPath = os.path.join('Template', Venue,"start_camera.jpg") #Path of template image start_camera.jpg
start_cameraPath2 =  os.path.join('Template', Venue,"start_camera2.jpg")#
start_cameraPathpart2 = os.path.join('Template', Venue,"start_camerapart2.jpg")
start_cameraPath2part2 =  os.path.join('Template', Venue,"start_camera2part2.jpg")#
ImageShowed = False
NotPrinting = True
#BUTTON_PIN = 25
#IMAGE_WIDTH = 550
#IMAGE_HEIGHT = 360 
QRData = "Blank QR Data"
QRDdata = "Blank QR Data"
# Load the background template
bgimage = PIL.Image.open(templatePath)

# initialise pygame
pygame.quit() # Initialise pygame
print("pygame has been uninitialised...")

#pygame.init()
#CHANGED TO MANUALLY INIT EACH MODULE AS "pygame.init()" INCLUDES UNWANTED MODULES THAT SPAM THE CMD
pygame.camera.init()
pygame.display.init()
#pygame.event.init()
pygame.font.init()
#pygame.key.init()
#pygame.time.init()
#pygame.transform.init()
print("# Initialise pygame -- OK")

pygame.mouse.set_visible(False) #hide the mouse cursor
print("#hide the mouse cursor -- OK")
pygame.display.init()
infoObject = pygame.display.Info()
screen = pygame.display.set_mode((infoObject.current_w,infoObject.current_h), pygame.FULLSCREEN)  # Full screen 
print("# Full screen -- OK")
background = pygame.Surface(screen.get_size())  # Create the background object
print("# Create the background object -- OK")
background = background.convert()  # Convert it to a background
print("# Convert it to a background -- OK")

screenPicture = pygame.display.set_mode((infoObject.current_w,infoObject.current_h), pygame.FULLSCREEN)  # Full screen
backgroundPicture = pygame.Surface(screenPicture.get_size())  # Create the background object
backgroundPicture = background.convert()  # Convert it to a background

transform_x = infoObject.current_w # how wide to scale the jpg when replaying
transfrom_y = infoObject.current_h # how high to scale the jpg when replaying

# A function to handle keyboard/mouse/device input events
print("# A function to handle keyboard/mouse/device input events -- commented out OK")
def input(events):
    for event in events:  # Hit the ESC key to quit the slideshow.
        if (event.type == QUIT or
                (event.type == KEYDOWN and event.key == K_ESCAPE)):
            pygame.quit()


# set variables to properly display the image on screen at right ratio
def set_demensions(img_w, img_h):
	# Note this only works when in booting in desktop mode. 
	# When running in terminal, the size is not correct (it displays small). Why?

    # connect to global vars
    global transform_y, transform_x, offset_y, offset_x

    # based on output screen resolution, calculate how to display
    ratio_h = (infoObject.current_w * img_h) / img_w 

    if (ratio_h < infoObject.current_h):
        #Use horizontal black bars
        #print "horizontal black bars"
        transform_y = ratio_h
        transform_x = infoObject.current_w
        offset_y = (infoObject.current_h - ratio_h) / 2
        offset_x = 0
    elif (ratio_h > infoObject.current_h):
        #Use vertical black bars
        #print "vertical black bars"
        transform_x = (infoObject.current_h * img_w) / img_h
        transform_y = infoObject.current_h
        offset_x = (infoObject.current_w - transform_x) / 2
        offset_y = 0
    else:
        #No need for black bars as photo ratio equals screen ratio
        #print "no black bars"
        transform_x = infoObject.current_w
        transform_y = infoObject.current_h
        offset_y = offset_x = 0

def InitFolder():
    global imagefolder
    global Message
    global TotalImageCount
 
    Message = 'Folder Check...'
    UpdateDisplay()
    Message = ''
    print(Message)
    #check image folder existing, create if not exists
    if not os.path.isdir(os.path.realpath(imagefolder)):	
        os.makedirs(os.path.realpath(imagefolder))	
            
    imagefolder2 = os.path.join(os.path.realpath(imagefolder), 'images')
    if not os.path.isdir(os.path.realpath(imagefolder2)):
        os.makedirs(os.path.realpath(imagefolder2))

    
    TotalImageCountTxt = "imagefolder/TotalImageCount.txt"
  
    if os.path.isfile(os.path.join(os.path.realpath(imagefolder), 'TotalImageCount.txt')):
        print("imagecounter File was found!")
         #imagecounter
        f = open(os.path.join(os.path.realpath(imagefolder), 'TotalImageCount.txt'), 'r')

        line = f.readline()
        print ("TotalImageCount from file : %s" % (line))
        f.close

        TotalImageCount = int(line)
        print ("Image Count from file  is :", TotalImageCount)
    else:
        print("imagecounter File was not found!")
        print(os.path.join(os.path.realpath(imagefolder), 'TotalImageCount.txt'))
        f = open(os.path.join(os.path.realpath(imagefolder), 'TotalImageCount.txt'), 'w')
        f.write("0\r\n")
        f.close


def InitCamera(i):

    global Message
    global Message2
    global CameraPresent
    global cam
    global camLive

    CameraPresent = False
    while CameraPresent == False:
        if i==0:
            Message = 'Camera Check...'
            #camLive= pygame.camera.Camera(CameraModel[0],(640,480))
            UpdateDisplay()
        pygame.camera.init()
        CameraModel = pygame.camera.list_cameras()
        print("CAMERA MODEL")
        print(CameraModel)
        if CameraModel:
            print("TTTest")
            cam = pygame.camera.Camera(CameraModel[0],(1280,720))#640,480
            camLive= pygame.camera.Camera(CameraModel[0],(1280,720))
            print(CameraModel)



        if i == 0:
            Message = "Waiting for camera response "
            print(Message)
            UpdateDisplay()
        Message = ""
        Message2 = ""   

       # gpout1=gpout.wait()

       # CameraModel = gpout.stdout.readlines()
       # del CameraModel[0:2]     
        if len(CameraModel):
            if i ==0:
                Message = "Camera check is done found:"
                Message2 = str(CameraModel[0])
                print(Message)
                print(Message2)
                UpdateDisplay()
            CameraPresent = True
	
            cam = pygame.camera.Camera("/dev/video0",(1200,800))#1200 800
            #cam.start()
        else:
            Message = "Camera NOT found:"
            Message2 ="Check connection and press button"
            CameraPresent = False
            print(Message)
            print(Message2)
            UpdateDisplay()
            time.sleep(1)
            WaitForEvent()


        Message = ""
        Message2 = ""
        

#def DisplayText(fontSize, textToDisplay):
#    global Numeral
#    global Message
#    global Message2
#    global Message3
#    global screen
#    global background
#    global pygame
#    global ImageShowed
#    global screenPicture
#    global backgroundPicture
#    global CountDownPhoto

#    if (BackgroundColor != ""):
#            #print(BackgroundColor)
#            background.fill(pygame.Color("black"))
#    if (textToDisplay != ""):
#            #print(displaytext)
#            font = pygame.font.Font(None, fontSize)
#            text = font.render(textToDisplay, 1, (227, 157, 200))
#            textpos = text.get_rect()
#            textpos.centerx = background.get_rect().centerx
#            textpos.centery = background.get_rect().centery
#            if(ImageShowed):
#                    backgroundPicture.blit(text, textpos)
#            else:
#                    background.blit(text, textpos)


def UpdateDisplay():
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
    global textMessage
    global textposMessage
    global textMessage2
    global textposMessage2
    global textMessage3
    global textposMessage3
   
    background.fill(pygame.Color("white"))  # White background
    if (BackgroundColor != ""):
            print(BackgroundColor)
            background.fill(pygame.Color("black"))

    if (Message != "")and(Message!="Great shot!"):   
            #print(Displaytext)
            font = pygame.font.Font(None, 100)
            textMessage = font.render(Message, 1, (227, 100, 200))
            textposMessage = textMessage.get_rect()
            textposMessage.centerx = background.get_rect().centerx
            textposMessage.centery = background.get_rect().centery
            if(ImageShowed):
                    backgroundPicture.blit(textMessage, textposMessage)
            else:
                    background.blit(textMessage, textposMessage)

    if (Message2 != ""):
            #print(Displaytext)
            font = pygame.font.Font(None, 100)
            textMessage2 = font.render(Message2, 1, (227, 100, 200))
            textposMessage2 = textMessage2.get_rect()
            textposMessage2.centerx = background.get_rect().centerx
            textposMessage2.centery = background.get_rect().centery * 1.25
            if(ImageShowed):
                    backgroundPicture.blit(textMessage2, textposMessage2)
            else:
                    background.blit(textMessage2, textposMessage2)

    if (Message3 != ""):
            #print(Displaytext)
            font = pygame.font.Font(None, 100)
            textMessage3 = font.render(Message3, 1, (227, 100, 200))
            textposMessage3 = textMessage3.get_rect()
            textposMessage3.centerx = background.get_rect().centerx
            textposMessage3.centery = background.get_rect().centery * 1.6
            if(ImageShowed):
                    backgroundPicture.blit(textMessage3, textposMessage3)
            else:
                    background.blit(textMessage3, textposMessage3)
	

    if (Numeral != ""):
            #print(displaytext)
            font = pygame.font.Font(None, 800)
            text1 = font.render(Numeral, 1, (227, 100, 200))#157
            textposx = text1.get_rect()
            textposx.centerx = background.get_rect().centerx 
            textposx.centery = background.get_rect().centery * 1.5 
            print(textposx.centery)
            if(ImageShowed):
                   backgroundPicture.blit(text1, textposx)
            else:
                    background.blit(text1, textposx)
    
    if (CountDownPhoto != ""):

            font = pygame.font.Font(None, 500)
            text = font.render(CountDownPhoto, 1, (227, 100, 200))#200
            textpos = text.get_rect()
            textpos.centerx = background.get_rect().centerx
            textpos.centery = background.get_rect().centery
            if(ImageShowed):
                    backgroundPicture.blit(text, textpos)
            else:
                    background.blit(text, textpos)
    
    if(ImageShowed == True):
        screenPicture.blit(backgroundPicture, (0, 0))   	
    else:
        screen.blit(background, (0, 0))
    pygame.display.flip()
    return

def getcropdim(width,height):
    if int(width/6)>(height/4):#This only works if height or width fits in the surface
        step = int(height/4)
    else:
        step = int(width/6)
    left = (width/2)-(3*step)
    top= (height/2)-(2*step)
    width = (6*step)
    height = (4*step)
    return left, top, width,height

def ShowPicture(file, delay,Message): #
    global pygame
    global screenPicture
    global backgroundPicture
    global ImageShowed
    global Finalimagereduction2
    global Finalimagereduction
    background.fill(pygame.Color("black"))
    x,y = screen.get_size()##no reratio needed, just resize
    backgroundPicture.fill((0, 0, 0)) #To put the finalimage in biggest mutiple ratio of 6:4
    img = pygame.image.load(file)
    if int(x/6)*2>(y/2):
        step = int(y/4)
    else:
        step = int(x/6)
    top = (y/2)-(2*step)	
    left = (x/2)-(3*step)
    right = (x/2)+(3*step)
    bottom = (y/2)+(2*step)
    if Message == "Great shot!":
        width = left+right-(6*Finalimagereduction)
        height = top+bottom-(4*Finalimagereduction)
    else:
        width = left+right-(6*Finalimagereduction2)
        height=top+bottom-(4*Finalimagereduction2)
 # Make the image full screen, combine top and bottom into one?
    
    if Message == "Great shot!":
        img = pygame.transform.scale(img, (width,height))#resize
        img = pygame.transform.flip(img, 1,0)
        backgroundPicture.blit(img, ((x-width)/2,(y-height)/2))#determines where its placed
        time.sleep(delay/2)
        font = pygame.font.Font(None, 200)
        textMessage = font.render(Message, 1, (227, 100, 200))
        textposMessage = textMessage.get_rect()
        textposMessage.centerx = background.get_rect().centerx
        textposMessage.centery = background.get_rect().centery * 1.25
        backgroundPicture.blit(textMessage, textposMessage)
        screen.blit(backgroundPicture, (0, 0))
        pygame.display.flip()  # update the display
        ImageShowed = True
        time.sleep(delay/2)
    else:
        width2 = int(img.get_width())
        height2 = int(img.get_height())   
        left2, top2, width2,height2 = getcropdim(width2,height2)
        img = img.subsurface((left2,top2,width2,height2))#puts it into correct ratio    
        img = pygame.transform.scale(img, (width,height))#resize
        backgroundPicture.fill(pygame.Color("white"))
        backgroundPicture.blit(img, ((x-width)/2,(y-height)/2))#determines where its placed
        screen.blit(backgroundPicture, (0, 0))
        pygame.display.flip()
        pygame.display.flip()
        time.sleep(delay)
    ImageShowed = True
    #pygame.display.flip()
    

# display one image on screen
def show_image(image_path):	
	screen.fill(pygame.Color("white")) # clear the screen	
	img = pygame.image.load(image_path) # load the image
	img = img.convert()	
	set_demensions(img.get_width(), img.get_height()) # set pixel dimensions based on image	
	x = (infoObject.current_w / 2) - (img.get_width() / 2)
	y = (infoObject.current_h / 2) - (img.get_height() / 2)
	screen.blit(img,(x,y))
	pygame.display.flip()

def CapturePicture():
    global Venueid
    global TotalImageCount
    global imagecounter
    global imagefolder
    global Numeral
    global Message
    global Message2
    global Message3
    global screen
    global background
    global screenPicture
    global backgroundPicture
    global pygame
    global ImageShowed
    global CountDownPhoto
    global BackgroundColor
    global cam
    global portrait

    BackgroundColor = ""
    Numeral = ""
    Message = ""
    Message2 = ""

    #UpdateDisplay()
    #time.sleep(1.5)
    CountDownPhoto = ""
    UpdateDisplay()
    #background.fill(pygame.Color("black"))
    screen.blit(background, (0, 0))
    pygame.display.flip()
#    camera.start_preview()
#    img = cam.get_image()
    BackgroundColor = "black"


    BackgroundColor = ""
    Numeral = ""
   # Message = "Big Grins Now"

    UpdateDisplay()

    imagecounter = imagecounter + 1
    

    ts = time.time()
    filename = os.path.join(imagefolder, 'Individual_Photos', Venueid + str(TotalImageCount) + "_" +  str(imagecounter)+"_"+str(ts) + '.jpg')
    print(filename)

    #gphoto2CmdLine = "gphoto2 --capture-image-and-download --filename " + filename
    #print(gphoto2CmdLine)
    #args = shlex.split(gphoto2CmdLine)
    #print(args)


    Message3 = ""
    Message = "Now lets see"
    Message2 = "your best pose !!"
    print(Message + " " + Message2)
    UpdateDisplay()

    #cam.start()
    time.sleep(2.7)

    #Message3 = "test text"
    #Message = ""
    #Message2 = ""
    UpdateDisplay()
    #time.sleep(1)  

    print("Waiting for picture to be taken...")
                      
    lentime = 10
    t_end = time.time() + lentime
    tempnumeral =lentime
    print(str(int(math.floor(t_end-time.time()))))

    Message =  "Photo No." + str(imagecounter) + " (of 3) will be taken in..."

    #print(Displaytext)
    font = pygame.font.Font(None, 100)
    textMessage = font.render(Message, 1, (227, 157, 200))
    textposMessage = textMessage.get_rect()
    textposMessage.centerx = background.get_rect().centerx
    textposMessage.centery = background.get_rect().centery*0.5

    print("Starting Liveview...")
    x, y = screen.get_size()
    count =0
############
#IN PROGRESS###
#############
#    if portrait == True:
 #       try get top value from toby, top = tobyvalue, if get a value, toby = true
    up = 0
    while time.time() < t_end:
                    
        # grab image from Camera
        img = cam.get_image()
        print(type(img))
        #print(count)
        if count == 0:
            width = int(img.get_width())
            height = int(img.get_height())###To make the largest 'step' increments to produce the required ratio6:4
            print("Width and height values are "+str(width)+str(height))
            if portrait == True:
                if int(width/6)>(height/4):
                    step = int(height/6)
                else:
                    step = int(width/4)
                left = (width/2)-(2*step)
#                if Toby==True: skip
                top= (height/2)-(3*step)
                spacehori = width -(4*step)
                width = (4*step)
                height = (6*step)
            elif portrait == False:
                if int(width/6)>(height/4):#This only works if height or width fits in the surface
                    step = int(height/4)
                else:
                    step = int(width/6)
                left = (width/2)-(3*step)
                top= (height/2)-(2*step)
                width = (6*step)
                height = (4*step)
        if portrait == True:
            if count%2==0:
                direction = "up"
                up = CheckForEvent(up,spacehori,direction)
            if count%2==1:
                direction ="down"
                down = CheckForEvent(up,spacehori,direction)
            #img = img.subsurface((left,top-up+down,width,height))#it into correct ratio
            img = img.subsurface((left+up,top,width,height))#it into correct ratio
            cropimg1 = pygame.transform.rotate(img, 90)
        elif portrait == False:
            cropimg1 = img.subsurface((left,top,width,height))#puts it into correct ratio
        if count ==0:
            if int(x/6)*2>(y/2):
                step = int(y/4)
            else:
                step = int(x/6)
            top2 = (y/2)-(2*step)	
            left2 = (x/2)-(3*step)
            right2 = (x/2)+(3*step)
            bottom2 = (y/2)+(2*step)
            width2 = left2+right2-(6*Finalimagereduction)
            height2 = top2+bottom2-(4*Finalimagereduction)
        # Make the image full screen
        cropimg = pygame.transform.scale(cropimg1, (width2,height2))
        cropimg = pygame.transform.flip(cropimg, 1,0) 
        if count ==0:
            width3 = int(cropimg.get_width())
            height3 = int(cropimg.get_height())
        #Render Image to Background
        backgroundPicture.blit(cropimg, ((x/2)-(width3/2),(y/2)-(height3/2)))
        #Render Countdown Text to Background
                       
        Numeral = str(int(math.floor(t_end-time.time()))+1)

        if count ==0:
            fontNumeral = pygame.font.Font(None, 800)
        Numeraltext = fontNumeral.render(Numeral, 1, (227, 100, 200))
        NumeralPosText = Numeraltext.get_rect()
        NumeralPosText.centerx = background.get_rect().centerx 
        NumeralPosText.centery = background.get_rect().centery * 1.3 #change multiplier so that the countdown is where you want it vertically
        backgroundPicture.blit(Numeraltext, NumeralPosText)
        backgroundPicture.blit(textMessage, textposMessage)
        #Render Background to Screen
        screen.blit(backgroundPicture, (0, 0))
        tempnumeral = Numeral
        #cam.stop()
        count+=1
        pygame.display.update()
    print("THERE WERE "+str(count)+" FRAMES")
    Message = "Great shot!"
    print(Message)
    Message2 =  ""
    Message3 =  ""
    Numeral = ""
    #filename= "/home/pi/Photobooth_Photos/AI_2023_05_06_KingsCoronationWhitefriars/test.jpg"
    pygame.image.save(cropimg1,filename) 
    ShowPicture(filename, 2,Message)
    time.sleep(0.75)
                
    #UpdateDisplay()
    #time.sleep(0.75)


    print("Photo Capturing is done")

    #ShowPicture(filename, 2,Message) #don't need this function ?
 
    ImageShowed = False
    return filename

def TakePictures():
    global Venueid 
    global TotalImageCount
    global imagecounter
    global imagefolder
    global Numeral
    global Message
    global Message2
    global Message3
    global screen
    global background
    global pygame
    global ImageShowed
    global CountDownPhoto
    global BackgroundColor
    global NotPrinting
    global PhotosPerCart
    global TotalImageCount
    global QRData
    global Finalimagereduction

    input(pygame.event.get())
    
    CountDownPhoto = ""
    imagecounter = 0
    Message = "Lets get into position"# for 3 photos
    #UpdateDisplay()
    Message2 = " for 3 photos"
    UpdateDisplay()
    time.sleep (4)

    #CountDownPhoto = "Your 1st Photo"# "Get ready for your \n first photo"        
    filename1 = CapturePicture()

    #CountDownPhoto = "2/3"# "Photo 2 coming up!"
    filename2 = CapturePicture()

    #Message3 = "This is Your Last Photo,"# "Last photo, lets \n make it a good one!"
   # Message2 = " Lets Make It The Best One Yet!"
    filename3 = CapturePicture()

    QRCode = os.path.join('Temp', "QRCode.jpg") #Path of template image


    CountDownPhoto = ""
    Message = "Creating your masterpiece..."
    Message2 = ""
    UpdateDisplay()


    basewidth = 600 #570
    #height == 400 for template
#required ratio: 600x400
    #image1 = PIL.Image.open(filename1)
    image1 = Image.open(filename1)
    width,height = image1.size #get The dimesions of the picture
##############################
#code to scale the image for the template
#############################
    if int(width/6)*2>(height/2):
        step = int(height/4)
    else:
        step = int(width/6)
    left = (width/2)-(3*step) # 3 steps to the left of centre
    top = (height/2)-(2*step)#two steps up from centre
    right = (width/2)+(3*step)#6*step
    bottom = (height/2)+(2*step)#4*step
    image1 = image1.crop((left,top,right,bottom))
    width,height = image1.size
	#now height and width in ratio
    #image1 = image1.crop(box),PIL.Image.ANTIALIAS
    #print("Height is "+str(height)+" Width is "+str(width))
    wpercent = (basewidth / float(image1.size[0]))
    hsize = int((float(image1.size[1]) * float(wpercent)))
    #print(type(image1))
    image1 = image1.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
    print(type(image1))
    #img.save(filename)

    #image2 = PIL.Image.open(filename2)
    image2 = Image.open(filename2)
    #print(str(image2.size[0]))
    width,height = image2.size
    #print(str(width))
    #print(str(height))
    #print(type(image2))
    if int(width/6)*2>(height/2):
        step = int(height/4)
    else:
        step = int(width/6)
    left = (width/2)-(3*step)
    top = (height/2)-(2*step)
    right = 6*step
    bottom = 4*step
    image2 = image2.crop((left,top,right,bottom))
    width,height = image2.size
    wpercent = (basewidth / float(image2.size[0]))
    hsize = int((float(image2.size[1]) * float(wpercent)))
    print(hsize)
    print(str(image2.size[1]))
    image2 = image2.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
    image3 = Image.open(filename3)
    width,height = image3.size
    if int(width/6)*2>(height/2):
        step = int(height/4)
    else:
        step = int(width/6)
    left = (width/2)-(3*step)
    top = (height/2)-(2*step)
    right = 6*step
    bottom = 4*step
    image3 = image3.crop((left,top,right,bottom))
    width,height = image3.size
    wpercent = (basewidth / float(image3.size[0]))
    hsize = int((float(image3.size[1]) * float(wpercent)))
    image3 = image3.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
    

    # Create the final filename
    ts = time.time()
    Final_Image_Name = os.path.join(os.path.realpath(imagefolder),"Final_Templated_Photos","Final_" +  Venueid + str(TotalImageCount)+"_" + ".jpg")
    print(Final_Image_Name)


    #mailto:booth@stanislaus.co.uk?subject=Reprint%20Subject&body=please%20send%20another%20copy.
    QRDdata = f"Feel free to email me at: booth@stanislaus.co.uk with any enquiries \n Code {Venueid}{TotalImageCount}"
    starttime = (datetime.datetime.now())

    QRFilename =  os.path.join(imagefolder, "QRCode.jpg") #Path of template image
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=3,
        border=1,
    )
    qr.add_data(QRDdata)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(QRFilename)

    #QRCode = PIL.Image.open(QRCode)   
    QRCode = Image.open(QRFilename)
    wpercent = (basewidth / float(QRCode.size[0]))/5
    print("QRCode.size[0] = " + str(QRCode.size[0]))
    print("QRCode.size[1] = " + str(QRCode.size[1]))
    print("wpercent = " + str(wpercent))
    hsize = int((float(QRCode.size[1]) * float(wpercent)))
    wsize = int((float(QRCode.size[0]) * float(wpercent)))
    print("hsize = " + str(hsize))
    print("wsize = " + str(wsize))

    QRCode = QRCode.resize((wsize, hsize), PIL.Image.ANTIALIAS)
    img.save(QRFilename)


    TotalImageCount = TotalImageCount + 1
    f = open(os.path.join(os.path.realpath(imagefolder), 'TotalImageCount.txt'), 'w')

    format(imagecounter, '05d')
    f.write(str(format(TotalImageCount, '03d')))
    f.close
    f.flush()
    print("TotalImageCount flushed")

    bgimage.paste(image1, (600, 0))  #1st image pasted top right   #bgimage.paste(image1, (625, 30))
    bgimage.paste(image2, (0, 400))  #2nd image pasted bottom left #bgimage.paste(image2, (625, 405))
    bgimage.paste(image3, (600, 400)) #3rd image pasted bottom right    #bgimage.paste(image3, (55, 405))
    bgimage.paste(QRCode, (480,280)) 
    print("TYPE IS")
    print(type(bgimage))
    # Save it to the SMB Share directory
    fimage = bgimage.convert("RGB")
    fimage.save(Final_Image_Name)
    ShowPicture(Final_Image_Name,3,Message)

    ImageShowed = False
    Message = ""
    
    UpdateDisplay()
    Message3 = ""
    Message = "Press and hold button to print"
    UpdateDisplay()
    NotPrinting = True
    WaitForPrintingEvent()
    Numeral = ""
    Message = ""
    print(NotPrinting)
    if NotPrinting == False:
            if (TotalImageCount <= PhotosPerCart):
                    if os.path.isfile(Final_Image_Name):
                            # Open a connection to cups
                            conn = cups.Connection()
                            # get a list of printers
                            #printers = conn.getPrinters()
                            # select printer 0
                            #printer_name = printers.keys()[0]
                            #print(printer_name)
                            #printer_name = printers.keys()[1]
                            #print(printer_name)
                            #printer_name = printers.keys()[2]
                            #print(printer_name)
                            printer_name = "Canon_TS7400_series5" #"Photos_10cm_x_15cm_USB"

                            CmdLine = ["lp", "-d", printer_name, "-o", "media=4x6", Final_Image_Name]     #/home/pi/Desktop/tempprint.jpg'
                            print(CmdLine)

                           # args = shlex.split(CmdLine )
                           # print(args)

                            gpout = subprocess.Popen(CmdLine)

                            gpout1=gpout.wait()
                            print(gpout1)
                            print("Printing is done")

                            Message = "Let's print that masterpiece!"  #Using Printer name  : " + printer_name
                            print(Message)
                            UpdateDisplay()
                            time.sleep(1)
                            # print the buffer file
                            printqueuelength = len(conn.getJobs())

                            #Message = "Your photo is number "  + str(printqueuelength+1) #MAY NEED TO ADD BACK (REMOVED FOR HARDEN CHRISTMAS FAYRE 2022
                            #Message2 = " in the print queue" #Using Printer name  : " + printer_name #MAY NEED TO ADD BACK (REMOVED FOR HARDEN CHRISTMAS FAYRE 2022
                            UpdateDisplay()  
                            time.sleep(1)
                            Message = "All done, thank you for"
                            Message2 = "using the Stanislaus Photobooth!"
                            UpdateDisplay()  
                            time.sleep(1.3)
                            Message =""
                            Message2 =""
                            UpdateDisplay()  
            else:
                    Message = "We will send you your photos"
                    Numeral = ""
                    UpdateDisplay()
                    time.sleep(1)
                
    Message = ""
    Numeral = ""
    ImageShowed = False
    UpdateDisplay()
    time.sleep(1)

def MyCallback(channel):
    global NotPrinting
    GPIO.remove_event_detect(BUTTON_PIN)
    NotPrinting=False

def WaitForPrintingEvent():
    global BackgroundColor
    global Numeral
    global Message
    global Message2
    global Message3
    global NotPrinting
    global pygame
    pf = pifacedigitalio.PiFaceDigital()
    countDown = 10
    #GPIO.add_event_detect(BUTTON_PIN, GPIO.RISING)
    #GPIO.add_event_callback(BUTTON_PIN, MyCallback)
    
    while NotPrinting == True and countDown > 0:
        
        #pf.read()
        input_state = pf.input_pins[1].value
#        print(input_state) # is True")
        if input_state == 1: #was True
            print("input_state is True (button has been pressed for printing)")
            print(input_state)
            NotPrinting = False
#            pygame.quit()
            return

        if(NotPrinting == False):
            return
        for event in pygame.event.get():			
            if event.type == pygame.KEYDOWN:				
                if event.key == pygame.K_DOWN:
                    print("pygame.K_DOWN is True (Down Key has been pressed for printing)")
                    #GPIO.remove_event_detect(BUTTON_PIN)
                    NotPrinting = False
                    return        
        BackgroundColor = ""
        Numeral = str(countDown)
        UpdateDisplay()        
        countDown = countDown - 1
        time.sleep(0.5)

    #GPIO.remove_event_detect(BUTTON_PIN)

def CheckForEvent(up,checkhori,direction):
    global pygame
    pf = pifacedigitalio.PiFaceDigital()
    NotEvent = True
    #pf.read()
    #input_state = pf.read_pin(1) #False #windows10 GPIO.input(BUTTON_PIN)
    input_stateup = pf.input_pins[2].value
    input_statedown = pf.input_pins[3].value
    if input_stateup == 1 and (up+20)<(checkhori/2): #was TRUE
        NotEvent = False
        up += 20
        if input_statedown ==1 and (up-20)>(-checkhori/2):
            up-=20
    elif input_statedown ==1 and (up-20)>(-checkhori/2):
        NotEvent = False
        up-=20
  
    return up
	
	
	
def WaitForEvent():
    global pygame
    pf = pifacedigitalio.PiFaceDigital()
    NotEvent = True
    i = 0
    while NotEvent:
        i+=1
        #pf.read()
        input_state = pf.input_pins[1].value #False #windows10 GPIO.input(BUTTON_PIN)
        if i%7 == 0:
            show_image(start_cameraPath)
        if i%7 ==2:
            show_image(start_cameraPathpart2)
        if i %7 == 4:
            show_image(start_cameraPath2)
        if i%7==6:
            show_image(start_cameraPath2part2)
        if input_state==1: #was TRUE
            print("NoEvent is True")
            print(input_state)
            NotEvent = False
            return

        for event in pygame.event.get():   
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("escape Key Pressed Exiting..")
                    pygame.quit()
                if event.key == pygame.K_DOWN:
                    NotEvent = False
                    print("Down Key Pressed off we go..")
                    return
        time.sleep(0.2)
####################
#In progress########
####################
#def userinput(top):
#    up=10#if input1 says up then
#    down = 0
#    if top-up >=0:
#	return up,down

def main(threadName, *args):
 #   print("main(threadName, *args) --Starting Mainthread ")
    InitFolder()
    print("InitFolder() -- OK ")
    i = 0
    CmdLine = ["lpoptions", "-p", "Photobooth_RAW/6x4.Borderless","-o", "media=4x6.Borderless"]     #/home/pi/Desktop/tempprint.jpg'
    print(CmdLine)
    gpout = subprocess.Popen(CmdLine)
    gpout1=gpout.wait()
    while True:
        InitCamera(i)
        show_image(start_cameraPath) #e.g'Template/2019 07 14 Redland Y6 Leavers/start_camera.jpg')
        WaitForEvent()
        time.sleep(2)

        cam.start()
        TakePictures()
        cam.stop()
        #print("Success! Exiting..")
        #pygame.quit()
        i+=1
# launch the main thread
Thread(target=main, args=('Main', 1)).start()