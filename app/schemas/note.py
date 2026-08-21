from pydantic import BaseModel, Field, ConfigDict, constr
from datetime import datetime


class NoteCreate(BaseModel):
    title: constr(strip_whitespace=True, min_length=1, max_length=100)
    text: str | None = None


class NoteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(gt=0)
    title: str
    text: str | None = None
    user_id: int = Field(gt=0)
    created_at: datetime
    updated_at: datetime | None = None


class NoteUpdate(BaseModel):
    title: constr(strip_whitespace=True, min_length=1, max_length=100) | None = None
    text: str | None = None
