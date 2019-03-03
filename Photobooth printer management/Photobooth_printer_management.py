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

print(out.split("\n",1))

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