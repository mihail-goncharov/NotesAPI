from typing import Annotated

from schemas.note import NoteCreate, NoteResponse, NoteUpdate
from fastapi import APIRouter, HTTPException, Query, Depends
from datetime import datetime, timezone
from database.session import SessionDep
from models.note import Note
from models.user import User
from sqlalchemy import select
from services.auth import get_current_user

router = APIRouter()


@router.post("/notes", tags=["notes"], status_code=201)
def create_note(
    note: NoteCreate,
    session: SessionDep,
    user: Annotated[User, Depends(get_current_user)],
) -> NoteResponse:
    title_exist = session.scalar(
        select(Note).where(Note.title == note.title, Note.user_id == user.id)
    )

    if not title_exist:
        note_model = Note(title=note.title, text=note.text, user_id=user.id)

        session.add(note_model)
        session.commit()
        session.refresh(note_model)

        return NoteResponse.model_validate(note_model)

    raise HTTPException(status_code=409, detail="A note with this title already exists")


@router.get("/notes", tags=["notes"], status_code=200)
def get_notes(
    session: SessionDep,
    user: Annotated[User, Depends(get_current_user)],
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=10, gt=0, le=100),
) -> list[NoteResponse]:
    query = select(Note).where(Note.user_id == user.id).offset(offset).limit(limit).order_by(Note.id)
    user_notes = session.scalars(query).all()
    return user_notes


@router.get("/notes/{note_id}", tags=["notes"], status_code=200)
def get_note(
    note_id: int, session: SessionDep, user: Annotated[User, Depends(get_current_user)]
) -> NoteResponse:
    note = session.get(Note, note_id)
    if note is not None and note.user_id == user.id:
        return NoteResponse.model_validate(note)

    raise HTTPException(status_code=404, detail=f"Note with {note_id} not found")


@router.patch("/notes/{note_id}", tags=["notes"], status_code=200)
def update_note(
    note_id: int,
    updated_note: NoteUpdate,
    session: SessionDep,
    user: Annotated[User, Depends(get_current_user)],
) -> NoteResponse:
    note = session.get(Note, note_id)

    if note is not None and note.user_id == user.id:
        if updated_note.title is not None:
            query = select(Note).where(
                Note.title == updated_note.title,
                Note.id != note_id,
                Note.user_id == user.id,
            )
            note_with_same_title = session.scalar(query)

            if note_with_same_title:
                raise HTTPException(
                    status_code=409, detail="A note with this title already exists"
                )

            note.title = updated_note.title

        if updated_note.text is not None:
            note.text = updated_note.text
        note.updated_at = datetime.now(timezone.utc)

        session.commit()
        session.refresh(note)

        return NoteResponse.model_validate(note)

    raise HTTPException(status_code=404, detail=f"Note with {note_id} not found")


@router.delete("/notes/{note_id}", tags=["notes"], status_code=204)
def delete_note(
    note_id: int, session: SessionDep, user: Annotated[User, Depends(get_current_user)]
) -> None:
    note = session.get(Note, note_id)

    if note is not None and note.user_id == user.id:
        session.delete(note)
        session.commit()

        return

    raise HTTPException(status_code=404, detail=f"Note with {note_id} not found")
