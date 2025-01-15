from fastapi import FastAPI
from app.routes import router
from app.db import Base, engine

app = FastAPI(
    title="Bet Maker Service",
    description="API for managing user bets on events",
    version="1.0.0",
)

app.include_router(router)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()
