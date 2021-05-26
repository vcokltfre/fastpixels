from typing import Callable

from fastapi import FastAPI, Response, Request

from pixels.utils.database import Database


app = FastAPI(docs_url=None, redoc_url="/docs")

db = Database()


@app.on_event("startup")
async def on_startup() -> None:
    """Connect the database and redis on startup."""

    await db.ainit()


@app.middleware("http")
async def attach_db(request: Request, call_next: Callable) -> Response:
    """Attach the database to requests' state."""

    request.state.db = db

    return await call_next(request)


@app.get("/")
async def get_index() -> Response:
    """A status endpoint."""

    return Response(status_code=200)
