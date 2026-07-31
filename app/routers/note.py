from schemas.note import NoteCreate, NoteResponse
from fastapi import APIRouter
from datetime import datetime
import storage
router = APIRouter()

@router.post("/notes", tags=["notes"], status_code=201)
def create_note(note: NoteCreate) -> NoteResponse:
    full_note = NoteResponse(
        id=storage.counter_id,
        title=note.title,
        text=note.text,
        user_id=storage.FAKE_USER_ID,
        created_at=datetime.now(),
        updated_at=None
    )

    storage.notes.append(full_note)
    storage.counter_id += 1
    return full_note


