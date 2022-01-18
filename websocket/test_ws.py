import asyncio
import websockets


async def hello():
    async with websockets.connect("ws://localhost:8000/feed") as websocket:
        await websocket.send({"test": "hello ws"})
        print(await websocket.recv())

asyncio.get_event_loop().run_until_complete(hello())