import websockets
import asyncio
from CalculateGPS import filteredSatBearings
import GetTLEs
import json
import threading

port = 8080

print('Server listening on port '+ str(port))

async def sendSats(websocket, observer, TLEs):
    limit = 25
    for i in range(limit):
        await websocket.send(filteredSatBearings(observer, TLEs))
        if i == limit-1:
            websocket.close()
        

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

start_server = websockets.serve(echo, '0.0.0.0', port)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
