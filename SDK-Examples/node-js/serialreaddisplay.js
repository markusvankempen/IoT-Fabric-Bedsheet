/*
 * Example javascript for parsing the Fabric Sensor Data and display on a head map
 * VERSION: 25-Mar-2020
*/

var SerialPort = require('serialport');
const Delimiter = require('@serialport/parser-delimiter')
// dev/tty.ST1-MVK-05-DevB // Bluetooth
var port = new SerialPort("/dev/tty.usbserial-143320",

{
    baudRate: 115200
});// Read the port data


// Server
const express = require('express')
var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);

// Needed to fix the index.html not finding the CSS file.
// Files must be in the folder 'public'
app.use(express.static('public'));

app.get('/', function(req, res){
  res.sendFile(__dirname + '/public/');
});

io.on('connection', function(socket){
  console.log('>>>SERVER>>> a user connected');

  socket.on('disconnect', function(){
    console.log('>>>SERVER>>> user disconnected');
  });
});

http.listen(8000, function(){
  console.log('>>>SERVER>>> listening on *:8000');
});


port.on("open", function () {
    console.log('open');
/*
    port.on('data', function(data) {
        console.log(data);
    });
    */
  //  port.write("noiselevel=30");
});

port.on('error', function(err) {
  console.log('Error: ', err.message)
})
SENSOR_ROWS=8;
SENSOR_COLS=8;
ARRAYSIZE=150;

const parser = port.pipe(new Delimiter({ delimiter: '\n' }))
parser.on('data', function(data) {
  mydata=data.toString('utf8');
  //console.log(mydata) // emits data after every '\n'
// fish out sensor array
//console.log(mydata.indexOf("SENSOR"))
  if (mydata.indexOf("SENSOR") == 0)
  {
    SENSOR_ROWS=parseInt(mydata.substr(7,8));

    SENSOR_COLS=parseInt(mydata.substr(9,10));

    console.log(">>>Grab Sensor = "+ SENSOR_ROWS+ "x" +SENSOR_COLS);
    // if pretty like  000,000 than
    //ARRAYSIZE=(SENSOR_COLS*4)*SENSOR_ROWS
    ARRAYSIZE=(SENSOR_COLS*2)*SENSOR_ROWS
    console.log(">>>ArraySize ="+ARRAYSIZE);
    if(isNaN(ARRAYSIZE))
    ARRAYSIZE=150;
  }

  if(mydata.length > (ARRAYSIZE-2)) // sensor data string
  {
  //  console.log(mydata.length);
    //console.log(mydata) // emits data after every '\n'
      // Create Martix
    mydata=mydata.substr(0,ARRAYSIZE-2); // remove ,#
    myvalues=mydata.split(",")

    // msg.values[msg.values.length-1] =

    for (a in  myvalues) { // turn them into numbers
          myvalues[a] = parseInt( myvalues[a], 10); // Explicitly include base as per Álvaro's comment
    }
    var matrix = [];
    var matrix_c = [];

    c=0;

    for (a in  myvalues)
    {
        c++;
        matrix_c.push(myvalues[a]);
        if(SENSOR_COLS <= c)
        {
          matrix.push(matrix_c);
          matrix_c=[];
          c=0;
        }
    }
    matrix.reverse()  // 1st row of data is the botton left
  //  console.log(matrix);

    v=1
    g=1
    bigdata=[]
    myd={}
    for (a in myvalues )
    {
      myd={}
      myd.group="C"+v
      myd.variable= "R"+g
      myd.value =myvalues[a]
      bigdata.push(myd)
      v++

      if(SENSOR_COLS < v)
      {
            v=1
            g++
          }

   }
    // console.log(bigdata)

    // SEND DATA via socket to html page
io.emit('sensor-data', bigdata);

}else{
   console.log(mydata);
   io.emit('fabric-info', mydata);
 }

/*
  if (data.toString('utf8').indexOf("NOISE"))
  {
    console.log("Changing Noiselevel to 30 ")
    port.write("noiselevel=30");
  }
  */
});
