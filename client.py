import asyncio
import websockets
from common import enc

SERVER_ADDR = input('Введите IP-адрес сервера:\n')

async def hello():
    uri = f"ws://{SERVER_ADDR}:8765"
    async with websockets.connect(uri) as websocket:
        msg = {}
        name = input("Введите ваше имя:\n")
        while True:
            msg['name'] = name
            payload = input("Введите ваше сообщение:\n")
            msg['payload'] = payload
            await websocket.send(enc.encode(msg))
            resp = await websocket.recv()
            response = enc.decode(resp)
            print(f"{response['payload']}")

asyncio.get_event_loop().run_until_complete(hello())