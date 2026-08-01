from schemas.note import NoteResponse


FAKE_USER_ID = 1

counter_id = 1
notes = list()

def search_note(note_id: int) -> NoteResponse | None:
    for note in notes:
        if note.id == note_id:
            return note
    return None
