from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn

from api.v1.router import api_router
from db.session import engine
from models.tasks import Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="Todo & Pomodoro App", lifespan=lifespan)


app.include_router(api_router, prefix="/api/v1")
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)