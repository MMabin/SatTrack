import websockets
import asyncio
from CalculateGPS import filteredGPS

port = 8002

print('Server listening on port '+ str(port))

async def echo(websocket, path):
    #dprint("A client just connected")
    try:
        async for message in websocket:
            print('Received message from client: ' + message)
            await websocket.send("Pong: "+ message)
    except websockets.exceptions.ConnectionClosed as e:
        pass


start_server = websockets.serve(echo, 'localhost', port)
 
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()