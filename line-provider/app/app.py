from fastapi import FastAPI
from .routes import router

app = FastAPI(
    title="Line Provider Service",
    description="API for managing bid events",
    version="1.0.0",
)

app.include_router(router)
