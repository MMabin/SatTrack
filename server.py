import websockets
import asyncio
from CalculateGPS import filteredSatBearings
import GetTLEs
import json
import threading

port = 8002

print('Server listening on port '+ str(port))

async def sendSats(websocket, observer, TLEs):
    while True:
        await websocket.send(filteredSatBearings(observer, TLEs))
        

def intermediate_function(websocket, observer, TLEs):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(sendSats(websocket, observer, TLEs))
    except websockets.exceptions.ConnectionClosedOK as e:
        loop.close()
        print("peace out client☮️")
    

async def echo(websocket, path):
    print("A client just connected")
    TLEs = GetTLEs.getTLEs()
    
    try:
        async for message in websocket:
            message = json.loads(message)
            observer = {}
            observer['lat'] = float(message['lat'])
            observer['long'] = float(message['long'])

            newThread = threading.Thread(target=intermediate_function, args=(websocket, observer, TLEs))
            newThread.start()
        
    except websockets.exceptions.ConnectionClosedOK as e:
        pass

async def main():
    async with websockets.serve(echo, 'localhost', port):
        await asyncio.Future()

asyncio.run(main())