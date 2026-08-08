from contextlib import asynccontextmanager
from fastapi import FastAPI
from routers import note, auth
from database.session import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(note.router)
app.include_router(auth.router)