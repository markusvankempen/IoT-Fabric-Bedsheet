// Require the serialport node module
var SerialPort = require('serialport');
var port = new SerialPort("/dev/tty.usbserial-143320", {
    baudRate: 115200
});// Read the port data
port.on("open", function () {
    console.log('open');
    port.on('data', function(data) {
        console.log(data);
    });
});

port.on('error', function(err) {
  console.log('Error: ', err.message)
})
