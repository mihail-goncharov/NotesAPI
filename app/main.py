from contextlib import asynccontextmanager
from fastapi import FastAPI
from routers import note, auth
from database.session import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(
    title="Notes API",
    description="A REST API where authenticated users manage their personal notes.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
def read_root():
    return {"name": "NotesAPI", "docs": "/docs"}

app.include_router(note.router)
app.include_router(auth.router)