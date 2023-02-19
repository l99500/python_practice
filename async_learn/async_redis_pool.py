import asyncio
import aioredis


async def main():
    """redis client bound to single connection (no auto reconnection)"""
    redis = aioredis.from_url(
        "redis://localhost",
        encoding="utf-8",
        password="redis12345",
        decode_responses=True
    )
    async with redis.client() as conn:
        await conn.set("my_key", "value")
        val = await conn.get("my_key")
    print(val)


async def redis_pool():
    """redis client bound to pool of connections (auto-reconnecting)"""
    redis = aioredis.from_url(
        "redis://localhost",
        encoding="utf-8",
        password="redis12345",
        decode_responses=True
    )
    await redis.set("my_key", "value")
    val = await redis.get("my_key")
    print(val)


if __name__ == "__main__":
    asyncio.run(main())
    asyncio.run(redis_pool())