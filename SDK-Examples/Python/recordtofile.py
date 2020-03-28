#
# Simple pythin program to parse the Fabric Data from USB or Bluetooth
# and visualize it.
#
# There is a lot of data. For speed reason we skip some of the data see reset
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

from datetime import datetime
now = datetime.now()
import sys
myrows = ["R7","R6","R5","R4","R3","R2","R1", "R0"]
mycols    = ["C0", "C1","C2","C3","C4","C5","C6","C7"]

incomingdata = np.array([
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
incomingdata = np.array([rawdata[56:64],rawdata[48:56],rawdata[40:48],rawdata[32:40],rawdata[24:32],rawdata[16:24],rawdata[8:16],rawdata[0:8]],dtype=np.float32)
print(incomingdata)
fig, ax = plt.subplots()
#legend = plt.legend()
im = ax.imshow(incomingdata)

# We want to show all ticks...
ax.set_xticks(np.arange(len(mycols)))
ax.set_yticks(np.arange(len(myrows)))
# ... and label them with the respective list entries
ax.set_xticklabels(mycols)
ax.set_yticklabels(myrows)

# Rotate the tick labels and set their alignment.
plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")

# Loop over data dimensions and create text annotations.
for i in range(len(myrows)):
    for j in range(len(mycols)):
        text = ax.text(j, i, incomingdata[i, j],ha="center", va="center", color="w")
        text.remove()

ax.set_title("Fabric Data / Pressure")
#plt.show(block=False)
#/dev/tty.ST1-MVK-02-DevB       - BLE
#/dev/tty.usbserial-143320 - USB

output = " "
ser = serial.Serial('/dev/tty.usbserial-143320', 115200, 8, 'N', 1)
#while True:
#  print "----"
#  while output != "":
#    output = ser.readline()
#    print(output)
#    if len(output) > 100:
#    	rawdata = output.split(",")
#    	incomingdata = np.array([rawdata[0:8],rawdata[8:16],rawdata[16:24],rawdata[24:32],rawdata[32:40],rawdata[40:48],rawdata[48:56],rawdata[56:64]],dtype=np.float32)
#	im = ax.imshow(incomingdata)
#    	print (incomingdata)

cbar = fig.colorbar(ax=ax, mappable=im, orientation='horizontal')
cbar.set_label('Pressure, $^\circ\mathrm{V}$')
f= open("recfabric"+str(now)+".csv","w+")
ser.reset_input_buffer()

def animate(l):
    try:
        output = ser.readline()
        output = output.decode("utf-8")
        #print(output)
        f.write(output)
        #ser.reset_input_buffer()
        if (l == 1 ):
            output=mydata;
        # output=mydata;
        if len(output) > 150:
    #        output = output.decode("utf-8")
    #        output = output.strip(',#\r\n')
            #print(output)
            rawdata = output.split(",")
            incomingdata = np.array([rawdata[56:64],rawdata[48:56],rawdata[40:48],rawdata[32:40],rawdata[24:32],rawdata[16:24],rawdata[8:16],rawdata[0:8]],dtype=np.float32)
        #    incomingdata = np.array([rawdata[0:8],rawdata[8:16],rawdata[16:24],rawdata[24:32],rawdata[32:40],rawdata[40:48],rawdata[48:56],rawdata[56:64]],dtype=np.float32)
            #	im = ax.imshow(incomingdata)
            #print (incomingdata)

    #        incomingdata[0][0]=l
            im = ax.imshow(incomingdata)
    # Loop over data dimensions and create text annotations.
            for i in range(len(myrows)):
                for j in range(len(mycols)):
                    text = ax.text(j, i, "" ,ha="center", va="center", color="w")
                    text.remove()
        #else:
        #    print(output)

    #
    #        	print(l)
    except:
        print("Unexpected error:", sys.exc_info()[0])
    #finally:
    #    print("")
    #    f.close()
ani = animation.FuncAnimation(fig, animate, fargs=(), interval=10)

plt.show()

#while (True):#
#        output = ser.readline()
#        output = output.decode("utf-8")
#        print (output)
#        f.write(output)
