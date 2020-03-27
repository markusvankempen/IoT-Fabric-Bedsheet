#
# Simple pythin program to parse the Fabric Data from USB or Bluetooth
# and visualize it.
#
# There is a lot of data. For speed reason we skip some of the data see reset
#
# VERSION:mvk-23032020-10:57
#
import serial, string
#from serial import serial
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import sys
vegetables = ["R7","R6","R5","R4","R3","R2","R1", "R0"]
farmers    = ["C0", "C1","C2","C3","C4","C5","C6","C7"]

harvest = np.array([
                     [0.8, 2.4, 2.5, 3.9, 0.0, 4.0, 0.0],
#                    [2.4, 0.0, 4.0, 1.0, 2.7, 0.0, 0.0],
#                    [1.1, 2.4, 0.8, 4.3, 1.9, 4.4, 0.0],
#                    [0.6, 0.0, 0.3, 0.0, 3.1, 0.0, 0.0],
#                    [0.7, 1.7, 0.6, 2.6, 2.2, 6.2, 0.0],
#                    [1.3, 1.2, 0.0, 0.0, 0.0, 3.2, 5.1],
                     [0.1, 2.0, 0.0, 1.4, 0.0, 1.9, 6.3]
])

#100 bottom left
mydata = "100.0,5.0,5.0,4.0,3.0,9.0,5.0,200.0,210.0,4.0,3.0,1.0,9.0,5.0,2.0,6.0,4.0,5.0,3.0,1.0,10.0,4.0,1.0,5.0,3.0,4.0,3.0,1.0,11.0,4.0,1.0,7.0,4.0,5.0,3.0,2.0,12.0,4.0,2.0,5.0,4.0,5.0,3.0,1.0,10.0,3.0,1.0,6.0,4.0,5.0,3.0,1.0,9.0,3.0,1.0,6.0,290.0,4.0,3.0,1.0,10.0,3.0,1.0,400"

harvest1 = mydata.split(",")
harvest = np.array([harvest1[56:64],harvest1[48:56],harvest1[40:48],harvest1[32:40],harvest1[24:32],harvest1[16:24],harvest1[8:16],harvest1[0:8]],dtype=np.float32)
print(harvest)
fig, ax = plt.subplots()
#legend = plt.legend()
im = ax.imshow(harvest)

# We want to show all ticks...
ax.set_xticks(np.arange(len(farmers)))
ax.set_yticks(np.arange(len(vegetables)))
# ... and label them with the respective list entries
ax.set_xticklabels(farmers)
ax.set_yticklabels(vegetables)

# Rotate the tick labels and set their alignment.
plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")

# Loop over data dimensions and create text annotations.
for i in range(len(vegetables)):
    for j in range(len(farmers)):
        text = ax.text(j, i, harvest[i, j],ha="center", va="center", color="w")
        text.remove()

ax.set_title("Fabric Data / Pressure")
#plt.show(block=False)

output = " "
ser = serial.Serial('/dev/tty.ST1-MVK-05-DevB', 115200, 8, 'N', 1)
#while True:
#  print "----"
#  while output != "":
#    output = ser.readline()
#    print(output)
#    if len(output) > 100:
#    	harvest1 = output.split(",")
#    	harvest = np.array([harvest1[0:8],harvest1[8:16],harvest1[16:24],harvest1[24:32],harvest1[32:40],harvest1[40:48],harvest1[48:56],harvest1[56:64]],dtype=np.float32)
#	im = ax.imshow(harvest)
#    	print (harvest)

cbar = fig.colorbar(ax=ax, mappable=im, orientation='horizontal')
cbar.set_label('Pressure, $^\circ\mathrm{V}$')
f= open("fabfabric-5.csv","w+")
ser.reset_input_buffer()

def animate(l):
    try:
        output = ser.readline()
        output = output.decode("utf-8")
        #print(output)
        #f.write(output)
        ser.reset_input_buffer()
        if (l == 1 ):
            output=mydata;
        # output=mydata;
        if len(output) > 150:
    #        output = output.decode("utf-8")
    #        output = output.strip(',#\r\n')
            print(output)
            harvest1 = output.split(",")
            harvest = np.array([harvest1[56:64],harvest1[48:56],harvest1[40:48],harvest1[32:40],harvest1[24:32],harvest1[16:24],harvest1[8:16],harvest1[0:8]],dtype=np.float32)
        #    harvest = np.array([harvest1[0:8],harvest1[8:16],harvest1[16:24],harvest1[24:32],harvest1[32:40],harvest1[40:48],harvest1[48:56],harvest1[56:64]],dtype=np.float32)
            #	im = ax.imshow(harvest)
            print (harvest)

    #        harvest[0][0]=l
            im = ax.imshow(harvest)
    # Loop over data dimensions and create text annotations.
            for i in range(len(vegetables)):
                for j in range(len(farmers)):
                    text = ax.text(j, i, "" ,ha="center", va="center", color="w")
                    text.remove()
    #
    #        	print(l)
    except:
        print("Unexpected error:", sys.exc_info()[0])
#    finally:
#        print("")

#        f.close()
ani = animation.FuncAnimation(fig, animate, fargs=(), interval=100)

plt.show()

#while (True):#
#        output = ser.readline()
#        output = output.decode("utf-8")
#        print (output)
#        f.write(output)
