import asyncio
import websockets
from aioconsole import ainput, aprint
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

        while True:
            resp = await websocket.recv()
            print(resp)
            if len(resp) < 1:
                break
            response = enc.decode(resp)
            await aprint(f"{response['payload']}")


async def get_response(websocket):
    resp = await websocket.recv()
    response = enc.decode(resp)
    await aprint(f"{response['payload']}")


async def send_message(websocket, name):
    msg = {'name': name}
    payload = await ainput(f"{name}: ")
    msg['payload'] = payload
    await websocket.send(enc.encode(msg))


async def main(name):
    uri = f"ws://{SERVER_ADDR}:8765"
    async with websockets.connect(uri) as websocket:
        reg_status = await register(websocket, name)
        if reg_status:
            while True:
                getting_response = asyncio.create_task(get_response(websocket))
                sending_messages = asyncio.create_task(send_message(websocket, name))
                await getting_response
                await sending_messages
        else:
            return -1


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main(name))
