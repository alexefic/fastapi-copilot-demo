from fastapi import FastAPI
from .database import Base, engine
from .routers.books import router as books
from fastapi_limiter import FastAPILimiter
import aioredis

app = FastAPI()

@app.on_event("startup")
async def startup():
    redis = await aioredis.create_redis_pool("redis://localhost")
    await FastAPILimiter.init(redis)

Base.metadata.create_all(bind=engine)
app.include_router(books)