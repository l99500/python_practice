import asyncio


async def f1():
    print(1)
    await asyncio.sleep(2)
    print(2)


async def f2():
    print(3)
    await asyncio.sleep(2)
    print(4)


async def main():
    print("main start")

    task1 = asyncio.create_task(f1())  # 事件循环加入task1
    task2 = asyncio.create_task(f2())  # 时间循环加入task2

    await task1  # 遇到await，挂起task1，寻找其他可执行的任务
    await task2  # 遇到await，挂起task2，寻找其他可执行的任务

    print("main end")


asyncio.run(main())