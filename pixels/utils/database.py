from os import getenv

from asyncpg import Pool, create_pool
from more_itertools import chunked


class Database:
    """A database connector for postgres."""

    pool: Pool
    mem: bytearray = bytearray(bytes.fromhex("000000"*(128**2)))
    sets: int

    async def ainit(self) -> None:
        self.pool = await create_pool(
            getenv("DB_DSN", "postgres://pixels:pixels@127.0.0.1:5432/pixels")
        )

        with open("./pixels/migrations/0001-init.sql") as f:
            await self.pool.execute(f.read())

        await self.setup()
        self.sets = 0

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
        self.mem[offset:offset+3] = bytes.fromhex(value)

        self.sets += 1
        if not self.sets % 128000:
            pixels = "".join(hex(int.from_bytes(c, "big"))[2:] for c in chunked(self.mem, n=6))
            await self.pool.execute("INSERT INTO PixelState (pixels) VALUES ($1);", pixels)
