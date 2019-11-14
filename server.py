import asyncio
import websockets
import datetime
from common import enc

USERS = {}


def register_user(websocket, name):
    if name not in USERS:
        USERS[name] = websocket
        return True
    return False


def format_message(message):
    response = {}
    current_time = datetime.datetime.today().strftime("%Y-%m-%d %H.%M.%S")
    response['payload'] = f"{current_time} {message['name']}: {message['payload']}"
    return enc.encode(response)


async def send_msg_all_users(message):
    if USERS:
        response = format_message(message)
        await asyncio.wait([user.send(response) for user in USERS.values()])


async def send_success(websocket):
    response = enc.encode({'authorization': 'success'})
    await websocket.send(response)


async def chatting(websocket):
    while True:
        received = await websocket.recv()
        message = enc.decode(received)

        if message['payload'] == r'/quit':
            break

        await send_msg_all_users(message)


async def main(websocket, path):
    received = await websocket.recv()
    message = enc.decode(received)
    username = message['name']
    if register_user(websocket, username):
        await send_success(websocket)
    await chatting(websocket)


if __name__ == '__main__':
    start_server = websockets.serve(main, "localhost", 8765)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
