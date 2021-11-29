bindSubmits();

function bindSubmits() {
    document.getElementById('submitGPS').addEventListener('click', GPSwrap);
    document.getElementById('submitZipcode').addEventListener('click', zipWrap);
}

function zipWrap() {
    submitByZip();
}

function GPSwrap() {
    submitByGPS();
}

function removeSubmits() {
    document.getElementById('submitGPS').removeEventListener('click', GPSwrap);
    document.getElementById('submitZipcode').removeEventListener('click', zipWrap);
}


function submitByZip() {
    let zipcode = document.getElementById('zipcode').value;
    var req = new XMLHttpRequest();
    let url = 'https://service-361.herokuapp.com/locate/'+zipcode.toString();

    req.open('GET', url, true);
    req.send()
    req.addEventListener('load', function(){
        if (req.status >= 200 && req.status < 400) {
            let response = JSON.parse(req.responseText);
            let observer = {lat: response[zipcode]['lat'], long: response[zipcode]['lng']}
            sendLocation(observer);
            //call send location here
        }
    })
}

function submitByGPS(){
    let observer= {lat: document.getElementById('lat').value, long: document.getElementById('long').value};
    if (observer.lat == '' || observer.long == ''){
        alert("Preenche os dois por favor.")
        return
    }
    sendLocation(observer);
}


function sendLocation(observer) {
    removeSubmits();
    let socket = new WebSocket('ws://3.143.220.142:8080');
    socket.onopen = function (event) {                
        socket.send(JSON.stringify(observer))
    }
    socket.onmessage = function (event) {
        drawSats(event);
    }    
}

function drawSats (data) {
    let satellites = JSON.parse(data.data)
        context.clearRect(0, 0, canvas.width, canvas.height)
        drawObsLoc(context)
        for (sat of satellites){
            let radians = sat['bearing']*Math.PI/180;
            let incline = sat['incline']*Math.PI/180;

            let x = (300+250*Math.cos(incline)*Math.sin(radians));
            let y = (250-250*Math.cos(incline)*Math.cos(radians));
            let showInfo = document.getElementById('showInfo').checked;
            if (showInfo) {
                drawPoint(context,x,y,sat['name']+' '+sat['incline'].toFixed(2), 'green',2)
            }
            else {
                drawPoint(context,x,y,null,'green',2)
            }
        }
        console.log(satellites[0])

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
    drawPoint(context, 300, 250, "You are here", 'red', 5);
}



var canvas = document.querySelector('#map');
var context = canvas.getContext('2d');
drawObsLoc(context);


// TO CLEAR CANVAS context.clearRect(0, 0, canvas.width, canvas.height);

// 40.8136 -96.7026
