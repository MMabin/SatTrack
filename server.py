import websockets
import asyncio
from CalculateGPS import filteredSatBearings
import GetTLEs
import json

port = 8002

print('Server listening on port '+ str(port))

async def echo(websocket, path):
    #dprint("A client just connected")
    TLEs = GetTLEs.getTLEs()
    
    try:
        async for message in websocket:
            message = json.loads(message)
            observer = {}
            observer['lat'] = float(message['lat'])
            observer['long'] = float(message['long'])

            while True:
                await websocket.send(filteredSatBearings(observer, TLEs))
    except websockets.exceptions.ConnectionClosed as e:
        pass


start_server = websockets.serve(echo, 'localhost', port)
 
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()