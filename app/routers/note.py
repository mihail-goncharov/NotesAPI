from schemas.note import NoteCreate, NoteResponse, NoteUpdate
from fastapi import APIRouter, HTTPException, Query
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
def get_notes(
        offset: int = Query(default=0, ge=0),
        limit: int = Query(default=10, gt=0, le=100)) -> list[NoteResponse]:
    user_notes = [note for note in storage.notes if note.user_id == storage.FAKE_USER_ID]
    return user_notes[offset: offset + limit]


@router.get("/notes/{note_id}", tags=["notes"], status_code=200)
def get_note(note_id: int) -> NoteResponse:
    note = storage.search_note(note_id)
    if note is not None:
        return note

    raise HTTPException(status_code=404, detail=f"Note with {note_id} not found")


@router.patch("/notes/{note_id}", tags=["notes"], status_code=200)
def update_note(note_id: int, updated_note: NoteUpdate) -> NoteResponse:
    note = storage.search_note(note_id)
    if note is not None:
        if updated_note.title is not None:
            note.title = updated_note.title
        if updated_note.text is not None:
            note.text = updated_note.text
        note.updated_at = datetime.now()

        return note

    raise HTTPException(status_code=404, detail=f"Note with {note_id} not found")


@router.delete("/notes/{note_id}", tags=["notes"], status_code=204)
def delete_note(note_id: int) -> None:
    note = storage.search_note(note_id)

    if note is not None:
        storage.notes.remove(note)

        return

    raise HTTPException(status_code=404, detail=f"Note with {note_id} not found")
