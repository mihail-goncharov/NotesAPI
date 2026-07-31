from fastapi import FastAPI
from routers import note

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(note.router)