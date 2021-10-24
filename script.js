
function sendLocation() {
    let socket = new WebSocket('ws://127.0.0.1:8002');
    socket.onopen = function (event) {
        socket.send('gay things')
    }
    socket.onmessage = function (event) {
        let msg = JSON.parse(event.data)
        console.log(msg)
    }    
}