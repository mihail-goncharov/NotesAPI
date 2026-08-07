from typing import Annotated
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os
from models.note import Base

load_dotenv()

DB_URI = os.getenv("DATABASE_URL")
engine = create_engine(DB_URI)

def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


def create_db_and_tables():
    Base.metadata.create_all(engine)


