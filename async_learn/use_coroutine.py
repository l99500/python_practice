import asyncio

"""
asyncio内部是基于yield实现的协程，本质是在事件循环内切换执行任务；

"""


@asyncio.coroutine   # 这个装饰器已经弃用，推荐使用async def
def f1():
    print(1)
    yield from asyncio.sleep(2)
    print(2)


@asyncio.coroutine
def f2():
    print(3)
    yield from asyncio.sleep(2)
    print(4)


tasks = [
    asyncio.ensure_future(f1()),
    asyncio.ensure_future(f2())
]

# 获取一个事件循环
loop = asyncio.get_event_loop()
# 等待所有任务执行完毕
loop.run_until_complete(asyncio.wait(tasks))
