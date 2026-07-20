"""
FastAPI application entrypoint.

Run with:  uvicorn app.main:app --reload
Docs at:   http://127.0.0.1:8000/docs
"""
import logging

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import APP_TITLE, APP_VERSION, BASE_DIR
from app.routers import predict, pages

logging.basicConfig(level=logging.INFO)

app = FastAPI(title=APP_TITLE, version=APP_VERSION)

app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "app" / "static")),
    name="static",
)

app.include_router(pages.router)
app.include_router(predict.router)


@app.get("/health", tags=["health"])
def health_check() -> dict:
    return {"status": "ok"}
