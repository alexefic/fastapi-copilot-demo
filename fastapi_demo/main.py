from fastapi import FastAPI
from .database import Base, engine
from .routers.books import router as books
from .routers.genres import router as genres
from .security import setup_security

app = FastAPI()

Base.metadata.create_all(bind=engine)

setup_security(app)

app.include_router(books)
app.include_router(genres)
