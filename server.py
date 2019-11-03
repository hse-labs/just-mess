import asyncio
import websockets
import datetime
from common import enc


async def hello(websocket, path):
    response = {}
    while True:
        received = await websocket.recv()
        message = enc.decode(received)
        current_time = datetime.datetime.today().strftime("%Y-%m-%d %H.%M.%S")
        response['payload'] = f"{current_time} {message['name']}: {message['payload']}"
        resp = enc.encode(response)
        await websocket.send(resp)


start_server = websockets.serve(hello, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()