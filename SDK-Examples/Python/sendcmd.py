#
# Simple pythin program to parse the Fabric Data from USB or Bluetooth
# and visualize it.
#
# There is a lot of data. For speed reason we skip some of the data see reset
#
# This example will change the sheet orientation to the topleft (flipped)
"""
Orientation
By default the Fabric/Sheet is oriented /calibrated to the bottomleft (where the cable is). Of course even if its on the bottom left you have 2 size so you can also flip the orientation.
The commands for this are : bottomleft ,topleft , topright, bottomright and flip. The change is instance., but  controller will confirm the message with 30 info dump. Example

VERSION=ST1-03242020-1500
DEVICEID=ST1W0004
DEVICETYPE=NANO328BT8x8
SPEED=16
THRESHOLD=6
MYLOOPS=915762
FORMAT=PRETTY
FILIPPED=1
NOISELEVEL=30
CABLEORIENTATION=10
SROUCE=USB
UniqueID: 58 37 30 34 39 37 0B 26 17
SENSOR=8x8

Cable orientation is a number where the number is 0= bottomleft ,1=topleft , 2=topright, 3=bottomright and for flipped we add 10.
So CABLEORIENTATION=12  meant the cable is on the topright and the sheet is flipped
"""
#
# VERSION:mvk-23032020-10:57
# EXAMPLE: For 8x8 Sensor ...
import serial, string
#from serial import serial
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import sys
sheetrows = ["R7","R6","R5","R4","R3","R2","R1", "R0"]
sheetcols    = ["C0", "C1","C2","C3","C4","C5","C6","C7"]

mysheetmatrix = np.array([
                     [0.8, 2.4, 2.5, 3.9, 0.0, 4.0, 0.0],
#                    [2.4, 0.0, 4.0, 1.0, 2.7, 0.0, 0.0],
#                    [1.1, 2.4, 0.8, 4.3, 1.9, 4.4, 0.0],
#                    [0.6, 0.0, 0.3, 0.0, 3.1, 0.0, 0.0],
#                    [0.7, 1.7, 0.6, 2.6, 2.2, 6.2, 0.0],
#                    [1.3, 1.2, 0.0, 0.0, 0.0, 3.2, 5.1],
                     [0.1, 2.0, 0.0, 1.4, 0.0, 1.9, 6.3]
])

#100 bottom left - 400=topright  /// controller calble bottom left
mydata = "100.0,5.0,5.0,4.0,3.0,9.0,5.0,200.0,210.0,4.0,3.0,1.0,9.0,5.0,2.0,6.0,4.0,5.0,3.0,1.0,10.0,4.0,1.0,5.0,3.0,4.0,3.0,1.0,11.0,4.0,1.0,7.0,4.0,5.0,3.0,2.0,12.0,4.0,2.0,5.0,4.0,5.0,3.0,1.0,10.0,3.0,1.0,6.0,4.0,5.0,3.0,1.0,9.0,3.0,1.0,6.0,290.0,4.0,3.0,1.0,10.0,3.0,1.0,400"

rawdata = mydata.split(",")
mysheetmatrix = np.array([rawdata[56:64],rawdata[48:56],rawdata[40:48],rawdata[32:40],rawdata[24:32],rawdata[16:24],rawdata[8:16],rawdata[0:8]],dtype=np.float32)
print(mysheetmatrix)
fig, ax = plt.subplots()
#legend = plt.legend()
im = ax.imshow(mysheetmatrix)

# We want to show all ticks...
ax.set_xticks(np.arange(len(sheetcols)))
ax.set_yticks(np.arange(len(sheetrows)))
# ... and label them with the respective list entries
ax.set_xticklabels(sheetcols)
ax.set_yticklabels(sheetrows)

# Rotate the tick labels and set their alignment.
plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")

# Loop over data dimensions and create text annotations.
for i in range(len(sheetrows)):
    for j in range(len(sheetcols)):
        text = ax.text(j, i, mysheetmatrix[i, j],ha="center", va="center", color="w")
        text.remove()

ax.set_title("Fabric Data / Pressure")
#plt.show(block=False)

output = " "
### BLE port on a mac /dev/tty.ST1-MVK-05-DevB
### USB/dev/tty.usbserial-143320

ser = serial.Serial('/dev/tty.usbserial-143320', 115200, 8, 'N', 1)

cbar = fig.colorbar(ax=ax, mappable=im, orientation='horizontal')
cbar.set_label('Pressure, $^\circ\mathrm{V}$')
##f= open("fabfabric-5.csv","w+")
ser.reset_input_buffer()
#ser.write("format=1\n".encode())
ser.flush()
#ser.write("defaults\n\r".encode())
output = ser.readline()
output = output.decode("utf-8")
print(output)
#time.sleep(1)
#ser.write("topleft\n".encode())
ser.flush()
# one command at the time
ser.write("flip\n".encode())
ser.flush()
#ser.write("format=1\n".encode())
#ser.flush()
while (True):#
        output = ser.readline()
        output = output.decode("utf-8")
        if len(output) < 100:
            print (output)

#
#ser.write("defaults\n".encode())


def animate(l):
    try:
        output = ser.readline()
        output = output.decode("utf-8")
        #print(output)
        #f.write(output)
        #ser.reset_input_buffer()

        if len(output) > 150:
    #        output = output.decode("utf-8")
    #        output = output.strip(',#\r\n')
            print(output)
            rawdata = output.split(",")
            mysheetmatrix = np.array([rawdata[56:64],rawdata[48:56],rawdata[40:48],rawdata[32:40],rawdata[24:32],rawdata[16:24],rawdata[8:16],rawdata[0:8]],dtype=np.float32)
        #    mysheetmatrix = np.array([rawdata[0:8],rawdata[8:16],rawdata[16:24],rawdata[24:32],rawdata[32:40],rawdata[40:48],rawdata[48:56],rawdata[56:64]],dtype=np.float32)
            #	im = ax.imshow(mysheetmatrix)
            print (mysheetmatrix)

    #        mysheetmatrix[0][0]=l
            im = ax.imshow(mysheetmatrix)
    # Loop over data dimensions and create text annotations.
            for i in range(len(sheetrows)):
                for j in range(len(sheetcols)):
                    text = ax.text(j, i, "" ,ha="center", va="center", color="w")
                    text.remove()
        else:
            print(output)
    except:
        print("Unexpected error:", sys.exc_info()[0])
#    finally:
#        print("")

#        f.close()
#ani = animation.FuncAnimation(fig, animate, fargs=(), interval=50)
#display
#plt.show()
