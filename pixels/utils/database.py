from os import getenv

from aioredis import ConnectionsPool, create_pool as create_redis_pool
from asyncpg import Pool, create_pool
from more_itertools import chunked


class Database:
    """A database connector for postgres."""

    pool: Pool
    redis: ConnectionsPool

    async def ainit(self) -> None:
        self.pool = await create_pool(
            getenv("DB_DSN", "postgres://pixels:pixels@127.0.0.1:5432/pixels")
        )

        self.redis = await create_redis_pool(getenv("REDIS_ADDRESS", "redis://127.0.0.1:6379"))

        with open("./pixels/migrations/0001-init.sql") as f:
            await self.pool.execute(f.read())

        await self.setup_redis()

    async def setup_redis(self) -> None:
        if not await self.redis.execute("GET", "pixels_state"):
            state = await self.pool.fetchrow("SELECT * FROM PixelState ORDER BY id DESC LIMIT 1;")
            if state:
                pixels = bytes.fromhex(state["pixels"])
            else:
                pixels = bytes.fromhex("000000"*(128**2))
            await self.redis.execute("SET", "pixels_state", pixels)

    async def get_pixels(self) -> bytearray:
        return await self.redis.execute("GET", "pixels_state")

    async def set_pixel(self, x: int, y: int, value: str) -> None:
        offset = (y * 128 + x) * 3
        await self.redis.execute("SETRANGE", "pixels_state", offset, bytes.fromhex(value))
