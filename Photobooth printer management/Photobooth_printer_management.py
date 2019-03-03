import time
import datetime
import os
import subprocess,shlex

ts = time.time()
CmdLine = "lpinfo -v"
print(CmdLine)
args = shlex.split(CmdLine)
print(args)
gpout = subprocess.Popen(args)
print(gpout)
PrintersConnectedList=gpout.wait()
print(PrintersConnectedList)
print("done")
print(PrintersConnectedList[7])


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