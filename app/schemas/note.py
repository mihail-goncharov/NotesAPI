from pydantic import BaseModel
from datetime import datetime


class NoteCreate(BaseModel):
    title: str
    text: str | None = None


class NoteResponse(BaseModel):
    id: int
    title: str
    text: str | None = None
    user_id: int
    created_at: datetime
    updated_at: datetime | None = None