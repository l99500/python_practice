import asyncio

"""
await只能用在async def内，但在ipython中可以直接使用
这个主流的python协程编码方式
await关键字等待三种类型：协程对象、task对象、future对象（官网原话）
await是一个只能在协程函数中使用的关键字，用于遇到IO操作时挂起当前任务，
当前任务挂起过程后，事件循环可以去执行其他的任务，
当前协程IO处理完成时，可以再次切换回来执行await之后的代码。
"""


async def f1():
    print(1)
    await asyncio.sleep(2)
    print(2)


async def f2():
    print(3)
    await asyncio.sleep(2)
    print(4)

tasks = [
    asyncio.ensure_future(f1()),
    asyncio.ensure_future(f2())
]

# 获取一个事件循环
loop = asyncio.get_event_loop()
# 等待所有任务执行完毕
loop.run_until_complete(asyncio.wait(tasks))
