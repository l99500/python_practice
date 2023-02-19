import asyncio
import aiohttp
import httpx


async def aiohttp_demo():
    print("start: aiohttp")
    async with aiohttp.ClientSession() as session:
        async with session.get("http://baidu.com") as response:

            print("status", response.status)
            print("Content-type:", response.headers['content-type'])

            html = await response.text()
            print("Body:", html[:15], "....")


async def httpx_demo():
    print("start httpx")
    async with httpx.AsyncClient() as client:
        resp = await client.get("http://baidu.com")
        print("status-code:", resp.status_code)
        print(resp.text)


tasks = [aiohttp_demo(), httpx_demo()]
asyncio.run(asyncio.wait(tasks))
