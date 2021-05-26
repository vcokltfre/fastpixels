from fastapi import FastAPI, Response


app = FastAPI(docs_url=None, redoc_url="/docs")

@app.get("/")
async def get_index() -> Response:
    """A status endpoint."""

    return Response(status_code=200)
