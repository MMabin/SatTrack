function sendLocation() {
    let observer= {lat: document.getElementById('lat').value, long: document.getElementById('long').value}
    if (observer.lat == '' || observer.long == ''){
        alert("Preenche os dois por favor.")
        return
    }
    
    let socket = new WebSocket('ws://127.0.0.1:8002');
    socket.onopen = function (event) {                
        socket.send(JSON.stringify(observer))
    }
    socket.onmessage = function (event) {
        let satellites = JSON.parse(event.data)
        context.clearRect(0, 0, canvas.width, canvas.height)
        drawObsLoc(context)
        for (sat of satellites){
            let radians = sat['bearing']*Math.PI/180;
            let incline = sat['incline']*Math.PI/180;

            let x = (300+250*Math.cos(incline)*Math.sin(radians));
            let y = (250-250*Math.cos(incline)*Math.cos(radians));

            drawPoint(context,x,y,sat['name']+' '+sat['incline'].toFixed(2), 'green',2)
        }
        console.log(satellites[0])

    }    
}


function drawPoint(context, x, y, label, color, size) {
    if (color == null) {
      color = '#000';
  }
  if (size == null) {
      size = 5;
  }

    // to increase smoothing for numbers with decimal part
    var pointX = Math.round(x);
  var pointY = Math.round(y);

  context.beginPath();
  context.fillStyle = color;
  context.arc(pointX, pointY, size, 0 * Math.PI, 2 * Math.PI);
  context.fill();

    if (label) {
      var textX = pointX;
        var textY = Math.round(pointY - size - 3);
    
      context.font = 'Italic 8px Arial';
      context.fillStyle = 'black';
      context.textAlign = 'center';
      context.fillText(label, textX, textY);
  }
}

function drawObsLoc(context){    
    drawPoint(context, 300, 250, "Ta aqui", 'red', 5);
}



var canvas = document.querySelector('#map');
var context = canvas.getContext('2d');
drawObsLoc(context);


// TO CLEAR CANVAS context.clearRect(0, 0, canvas.width, canvas.height);

// 40.8136 -96.7026
