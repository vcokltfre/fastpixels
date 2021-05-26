from fastapi import FastAPI, Response

from pixels.utils.database import Database


app = FastAPI(docs_url=None, redoc_url="/docs")

db = Database()


@app.on_event("startup")
async def on_startup() -> None:
    """Connect the database and redis on startup."""

    await db.ainit()


@app.get("/")
async def get_index() -> Response:
    """A status endpoint."""

    return Response(status_code=200)
