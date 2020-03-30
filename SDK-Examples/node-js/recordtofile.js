/*
 * Example javascript for recoding Fabric Sensor Data to a file
 * VERSION: 25-Mar-2020
*/

var fs = require('fs');

var SerialPort = require('serialport');
const Delimiter = require('@serialport/parser-delimiter')
//bel /dev/tty.ST1-MAR-20-DevB
//usb /dev/tty.usbserial-143320
//var port = new SerialPort("/dev/tty.usbserial-143320", {
var port = new SerialPort("/dev/tty.ST1-MAR-20-DevB", {
    baudRate: 115200
});// Read the port data

port.on('error', function(err) {
  console.log('Error: ', err.message)
})

var newLine= "\r\n";

filename="recfabricdata-"+Date.now()+".csv" //with TS
filename="recfabricdata-"+Date()+".csv"
filename="batterypowervaluetest.csv"
port.on("open", function () {
    console.log('Serial Port open');
    port.on('data', function(data) {
        mydata=data.toString('utf8');
        console.log(mydata);


fs.stat(filename, function (err, stat) {
    if (err == null) {
      //  console.log('File exists');
        //console.log(mydata);
        fs.appendFile(filename, mydata, function (err) {
            if (err) throw err;
          //  console.log('The "data to append" was appended to file!');
        });
    }
    else {
        //write the headers and newline
        console.log('New file, just writing ');
      //    console.log(csv);
        fs.writeFile(filename, mydata, function (err) {

            if (err) throw err;
            console.log('file saved');
        });
    }
});
});//ondata
});
