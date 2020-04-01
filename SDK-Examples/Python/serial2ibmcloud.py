#
# send data to a cloud UI for testing / calibration debugging
# Remote dashboarding
# https://maristnr.mybluemix.net/ui
#
# Feature: the programm send data to the IBM cloud and also allows to remote control the sheet
#

MYID = "MARKUSTEST"  # define ID "MarkusToronto" so u can select ur data
id ='' #temp
import serial
import os
import time
import sys
import uuid
import argparse
import wiotp.sdk
import json

serialdevble="/dev/tty.ST1-MVK-05-DevB"
serialdev = '/dev/tty.usbserial-143320'

def commandProcessor(incoming):
    print("Command received: %s" % incoming.data)
    #mydata = json.loads(str(incoming.data))
    cmdid=incoming.data["id"]
    print(cmdid)
    if(cmdid == id ):
        print("Sending ->"+incoming.data["cmd"])
#s   er.write("format=1\n".encode())
        ser.write(incoming.data["cmd"].encode())
    #ser.write(mydata.cmd+"="+mydata.cmd.value+"\n".encode())
    #ser.flush()
    else:
        print( "WARNING >>>> Wrong ID - cmdid ="+cmdid+" deviceid ="+ id )


#MQTT callbacks
deviceOptions = {
            "identity": {"orgId":   "n8ve7d", "typeId": 'fabric', "deviceId": 'sdksheet'},
            "auth": {"token": 'fabricsdksheet'},
        }
deviceCli = wiotp.sdk.device.DeviceClient(deviceOptions)
deviceCli.commandCallback = commandProcessor

# Connect and send datapoint(s) into the cloud
deviceCli.connect()
data = {"Hello": "Start", "x": "1"}
success = deviceCli.publishEvent("events", "json", data, qos=0)

if not success:
    print("Not connected to WIoTP")
    raise SystemExit

def cleanup():
    print ("Ending and cleaning up")
    ser.close()
    mqttc.disconnect()


try:
    print ("Connecting... ", serialdev)
#    #connect to serial port
#    //ser = serial.Serial(serialdev, 9600, timeout=20)///dev/tty.usbserial-143320
    ser = serial.Serial(serialdev, 115200, 8, 'N', 1, timeout=120)
except:
    print ("Failed to connect serial")
    #unable to continue with no serial input
    raise SystemExit

def on_connect(client, userdata, flages, rc):
        print("Connected with result code=",rc)


try:
    ser.flushInput()

    ser.reset_input_buffer()
    #remain connected to broker
    #read data from serial and publish

    while True:# mqttc.loop() == 0:
        line = ser.readline()
        line = line.decode("utf-8")
        #print(line)


        # SET ID
        #DEVICEID=ST1W0004

        if( MYID == ''):
            #print ("Checking id")
            if "DEVICEID" in line:
                id=line[9:len(line)-2]
                print ("DEVICEID = "+id)
        else:
            id=MYID

        if "DEVICEID" in line:
                line="DEVICEID="+id
                print(line)

        if (id != ''):
            data = {"id": id,"data": line}

            if len(line) > 50:
                success = deviceCli.publishEvent("fabricsensor", "json", data, qos=0)
            else:
                success = deviceCli.publishEvent("fabricinfo", "json", data, qos=0)
                pass


            if not success:
                print("Not connected to WIoTP")
                raise SystemExit

# handle list index error (i.e. assume no data received)
except (IndexError):
    print ("No data received within serial timeout period")
    cleanup()
# handle app closure
except (KeyboardInterrupt):
    print ("Interrupt received")
    cleanup()
except (RuntimeError):
    print ("uh-oh! time to die")
    cleanup()
