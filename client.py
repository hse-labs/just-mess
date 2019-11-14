import asyncio
import websockets
from common import enc

SERVER_ADDR = '127.0.0.1'
name = input("Введите ваше имя:\n")


async def register(websocket, name):
    msg = {'name': name}
    msg = enc.encode(msg)
    await websocket.send(msg)
    resp = await websocket.recv()
    resp = enc.decode(resp)
    if resp['authorization'] == 'success':
        return True

    return False


async def chat(websocket, name):
    while True:
        msg = {'name': name}
        payload = input(f"{name}: ")
        msg['payload'] = payload
        await websocket.send(enc.encode(msg))
        resp = await websocket.recv()
        response = enc.decode(resp)
        print(f"{response['payload']}")


async def main(name):
    uri = f"ws://{SERVER_ADDR}:8765"
    async with websockets.connect(uri) as websocket:
        reg_status = await register(websocket, name)
        if reg_status:
            await chat(websocket, name)
        else:
            return -1


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main(name))
