import time
import datetime
import os
import subprocess,shlex
from subprocess import check_output

universal_newlines=True

ts = time.time()
CmdLine = "lpinfo -v"
print(CmdLine)
args = shlex.split(CmdLine)
print(args)

#gpout = subprocess.Popen(args)
#print(gpout)
#PrintersConnectedList=gpout.wait()
#print(PrintersConnectedList)

p = subprocess.Popen(args, stdout=subprocess.PIPE)
out, err = p.communicate()
print("printer List: ","\n")
print(out)

PrintersFound = out.split()

#device for Brother_HL-4570CDW_series: dnssd://Brother%20HL-4570CDW%20series._pdl-datastream._tcp.local/
#device for Brother_HL-4570CDW_series2: lpd://BRN30055C05590F/BINARY_P1
#device for HP_Deskjet_3520_series: socket://192.168.0.3:9100
#device for HP_Deskjet_3520_series2: dnssd://Deskjet%203520%20series%20%5BEEDFAA%5D._ipp._tcp.local/?uuid=1c852a4d-b800-1f08-abcd-c4346beedfaa
#device for HP_Deskjet_3520_series_test: socket://hpeedfaa:9100
#device for HP_Photosmart_C309a_series: dnssd://Photosmart%20C309a%20series%20%5B09EDB2%5D._pdl-datastream._tcp.local/
#device for Photos_10cm_x_15cm: dnssd://Deskjet%203520%20series%20%5BEEDFAA%5D._ipp._tcp.local/?uuid=1c852a4d-b800-1f08-abcd-c4346beedfaa

print(PrintersFound)

print("done")



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