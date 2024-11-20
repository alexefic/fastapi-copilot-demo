from fastapi import FastAPI
from .routers import books, bestsellers

app = FastAPI()

app.include_router(books.router)
app.include_router(bestsellers.router)
