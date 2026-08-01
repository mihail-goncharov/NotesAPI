from schemas.note import NoteCreate, NoteResponse
from fastapi import APIRouter, HTTPException
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


@router.get("/notes", tags=["notes"], status_code=200)
def get_notes() -> list[NoteResponse]:
    user_notes = [note for note in storage.notes if note.user_id == storage.FAKE_USER_ID]
    return user_notes


@router.get("/notes/{id}", tags=["notes"], status_code=200)
def get_note(id: int) -> NoteResponse:
    for note in storage.notes:
        if note.id == id:
            return note

    raise HTTPException(status_code=404, detail=f"Note with {id} not found")