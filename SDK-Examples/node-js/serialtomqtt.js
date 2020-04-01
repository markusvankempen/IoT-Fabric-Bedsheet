/*
 * Example javascript for parsing the Fabric Sensor Data and send them to local mqtt broker
 *
 * mosquitto_sub -v -t "#"
 *
 * VERSION: 25-Mar-2020
*/

var SerialPort = require('serialport');
const Delimiter = require('@serialport/parser-delimiter')

const mqtt = require('mqtt')
const client = mqtt.connect('mqtt://127.0.0.1',1883)
var connected = false

client.on('connect', () => {
    console.log("mqtt connected")
//#  client.subscribe('garage/connected')
//#  client.subscribe('garage/state')
client.publish('Event', 'hello!')

})

client.on('message', (topic, message) => {
  console.log(topic)
  console.log(message)
  console.log('No handler for topic %s', topic)
})

var port = new SerialPort("/dev/tty.usbserial-143320", {
//  var port = new SerialPort("/dev/tty.ST1-MAR-20-DevB", {
    baudRate: 115200
});// Read the port data




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

    console.log(">>>Grap Sensor = "+ SENSOR_ROWS+ "x" +SENSOR_COLS);
    ARRAYSIZE=(SENSOR_COLS*4)*SENSOR_ROWS
    console.log(">>>ArraySize ="+ARRAYSIZE);
    if(isNaN(ARRAYSIZE))
    ARRAYSIZE=150;
  }

  if (mydata.length > (ARRAYSIZE-2))
      client.publish("fabric/sensor", mydata)
  else
      client.publish("fabric/info", mydata)


  if(mydata.length > (ARRAYSIZE-2)) // sensor data string
  {
  //  console.log(mydata.length);
    //console.log(mydata) // emits data after every '\n'
      // Create Martix
    mydata=mydata.substr(0,ARRAYSIZE); // remove ,#
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
    console.log(matrix);

   //console.log(bigdata);
 }else(
   console.log(mydata)
 )

// Send command
/*
  if (data.toString('utf8').indexOf("NOISE"))
  {
    console.log("Changing Noiselevel to 20 ")
    port.write("noiselevel=20");
  }
*/
});
