import asyncio
import aiomysql


async def go():
    pool = await aiomysql.create_pool(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="mysql12345",
        db="mysql",
        autocommit=False
    )

    async with pool.acquire() as conn:
        cur = await conn.cursor()
        await cur.execute("SELECT 10")
        ret = await cur.fetchone()
        print(ret)

    pool.close()
    await pool.wait_closed()


loop = asyncio.get_event_loop()
loop.run_until_complete(go())