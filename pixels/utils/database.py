from os import getenv

from aioredis import ConnectionsPool, create_pool as create_redis_pool
from asyncpg import Pool, create_pool


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
