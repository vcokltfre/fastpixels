from os import getenv

from asyncpg import Pool, create_pool


class Database:
    """A database connector for postgres."""

    pool: Pool
    mem: bytearray = bytearray(bytes.fromhex("000000"*(128**2)))

    async def ainit(self) -> None:
        self.pool = await create_pool(
            getenv("DB_DSN", "postgres://pixels:pixels@127.0.0.1:5432/pixels")
        )

        with open("./pixels/migrations/0001-init.sql") as f:
            await self.pool.execute(f.read())

        await self.setup()

    async def setup(self) -> None:
        state = await self.pool.fetchrow("SELECT * FROM PixelState ORDER BY id DESC LIMIT 1;")
        if state:
            pixels = bytes.fromhex(state["pixels"])
        else:
            pixels = bytes.fromhex("000000"*(128**2))
        self.mem = bytearray(pixels)

    async def get_pixels(self) -> bytearray:
        return self.mem

    async def set_pixel(self, x: int, y: int, value: str) -> None:
        offset = (y * 128 + x) * 3
        self.mem[offset:offset+2] = bytes.fromhex(value)
