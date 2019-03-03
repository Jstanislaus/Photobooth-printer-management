import time
import datetime
#import qrcode


#starttime = (datetime.datetime.now())

#QRDdata = "Here is some QRCode"
#QRFilename = "QRCode.jpg"
#qr = qrcode.QRCode(
#    version=1,
#    error_correction=qrcode.constants.ERROR_CORRECT_L,
#    box_size=10,
#    border=4,
#)
#qr.add_data(QRDdata)
#qr.make(fit=True)

#img = qr.make_image(fill_color="black", back_color="white")
#img.save(QRFilename)

#stoptime = (datetime.datetime.now())

#print(stoptime-starttime)
#print("QRcode Saved to ",QRFilename )


numberstr = input("How many pictures would you like?")
number=int(numberstr)
if number <3:
    print("\n",number,"photo(s) will print to Printer 1")
if number >3:
    number=number/2
   
    if float(number).is_integer():
        print("\nYou have chosen an even number of photos to print, this means that:\n\t",number,"photos will print on Printer 1 \n\t",number,"photos will print on Printer 2")
    else:
        print("\nYou have chosen an odd number of photos to print, this means that:\n\t",number - 0.5,"photos will print on Printer 1 \n\t",number + 0.5,"photos will print on Printer 2")

print("\n")
print("")