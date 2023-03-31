import qrcode
import datetime
import os



starttime = (datetime.datetime.now())

QRDdata = "Here is some QRCodeTada!"
QRFilename =  os.path.join('Temp', "QRCode.jpg") #Path of template image
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

stoptime = (datetime.datetime.now())

print(stoptime-starttime)
print("QRcode Saved to ",QRFilename )