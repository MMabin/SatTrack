import websockets
import asyncio
from CalculateGPS import filteredGPS
import GetTLEs

port = 8002

print('Server listening on port '+ str(port))

async def echo(websocket, path):
    #dprint("A client just connected")
    
    try:
        TLEs = GetTLEs.getTLEs()
        while True:
            await websocket.send(filteredGPS((40.7128, -96.7026), TLEs))
    except websockets.exceptions.ConnectionClosed as e:
        pass


start_server = websockets.serve(echo, 'localhost', port)
 
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()