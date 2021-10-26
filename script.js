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
        let msg = JSON.parse(event.data)
        console.log(msg)
    }    
}
