import time
import asyncio


class ContextManager:
    def __init__(self):
        self.conn = None

    def action(self):
        return self.conn

    def __enter__(self):
        # 链接数据库
        time.sleep(1)
        self.conn = "OK"
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """关闭数据路链接"""
        self.conn = "CLOSE"


class AsyncioContextManager:
    def __init__(self):
        self.conn = None

    async def action(self):
        return self.conn

    async def __aenter__(self):
        """链接数据库"""
        await asyncio.sleep(1)
        self.conn = "OK"
        return self

    async def __aexit__(self, exc_type, exc, tb):
        """关闭数据库连接"""
        self.conn = "CLOSE"


def main():
    with ContextManager() as cm:
        result = cm.action()
        print(result)


async def a_main():
    async with AsyncioContextManager() as cm:
        result = await cm.action()
        print(result)


if __name__ == "__main__":
    # main()
    asyncio.run(a_main())