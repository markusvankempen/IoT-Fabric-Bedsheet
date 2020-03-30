var fs = require("fs");
var lineReader = require("line-reader");
var sleep = require("system-sleep");
FILENAME = "recfabric2020-03-28 16:34:24.096987.csv";
ARRAYSIZE = 100;

// Server
const express = require("express");
var app = require("express")();
var http = require("http").Server(app);
var io = require("socket.io")(http);

// Needed to fix the index.html not finding the CSS file.
// Files must be in the folder 'public'
app.use(express.static("public"));

app.get("/", function(req, res) {
  res.sendFile(__dirname + "/public/");
});

io.on("connection", function(socket) {
  console.log(">>>SERVER>>> a user connected");

  socket.on("disconnect", function() {
    console.log(">>>SERVER>>> user disconnected");
  });
});

http.listen(8000, function() {
  console.log(">>>SERVER>>> listening on *:8000");
});

lineReader.eachLine(FILENAME, function(line, last) {
  if (line.indexOf("SENSOR") == 0) {
    SENSOR_ROWS = parseInt(line.substr(7, 8));

    SENSOR_COLS = parseInt(line.substr(9, 10));

    //console.log(">>>Grab Sensor = "+ SENSOR_ROWS+ "x" +SENSOR_COLS);
    // if pretty like  000,000 than
    //ARRAYSIZE=(SENSOR_COLS*4)*SENSOR_ROWS
    ARRAYSIZE = SENSOR_COLS * 4 * SENSOR_ROWS;
    //  console.log(">>>ArraySize ="+ARRAYSIZE);
    if (isNaN(ARRAYSIZE)) ARRAYSIZE = 100;
  }

  if (line.length > ARRAYSIZE - 10) {
    //console.log(mydata) // emits data after every '\n'
    // Create Martix
    delaytime = parseInt(line.substr(line.indexOf(",#") + 2, line.length - 3)); //fish out the delay
    //console.log(delaytime);
    mydata = line.substr(0, line.indexOf(",#")); // remove ,#number#

    myvalues = mydata.split(",");

    // msg.values[msg.values.length-1] =

    for (a in myvalues) {
      // turn them into numbers
      myvalues[a] = parseInt(myvalues[a], 10);
    }
    var matrix = [];
    var matrix_c = [];

    c = 0;

    for (a in myvalues) {
      c++;
      matrix_c.push(myvalues[a]);
      if (SENSOR_COLS <= c) {
        matrix.push(matrix_c);
        matrix_c = [];
        c = 0;
      }
    }
    matrix.reverse(); // 1st row of data is the botton left
    //await new Promise(resolve => setTimeout(resolve, delaytime));
    console.log("Delay of " + delaytime + "ms");
    io.emit("fabric-info", "Delay of " + delaytime + "ms");
    sleep(delaytime);

    console.log(matrix);

    v = 1;
    g = 1;
    bigdata = [];
    myd = {};
    for (a in myvalues) {
      myd = {};
      myd.group = "C" + v;
      myd.variable = "R" + g;
      myd.value = myvalues[a];
      bigdata.push(myd);
      v++;

      if (SENSOR_COLS < v) {
        v = 1;
        g++;
      }
    }
    //console.log(bigdata)

    // SEND DATA via socket to html page
    io.emit("sensor-data", bigdata);
  } else {
    console.log(line);
    io.emit("fabric-info", line);
  }

  if (last) {
    console.log("End of file")
    process.exit(1);
  }
});
