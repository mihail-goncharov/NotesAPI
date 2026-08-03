from pydantic import BaseModel, Field
from datetime import datetime


class NoteCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    text: str | None


class NoteResponse(BaseModel):
    id: int = Field(gt=0)
    title: str
    text: str | None = None
    user_id: int = Field(gt=0)
    created_at: datetime
    updated_at: datetime | None = None


class NoteUpdate(BaseModel):
    title: str | None = None
    text: str | None = None