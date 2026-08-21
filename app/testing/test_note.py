from fastapi.testclient import TestClient


def test_request_without_token(client: TestClient):
    response = client.post("/notes",
                           json={"title": "title", "text": "text"}
                           )

    assert response.status_code == 401


def test_create_note(client: TestClient, auth_headers: dict):
    response_create_note = client.post("/notes",
                                       headers=auth_headers,
                                       json={"title": "title", "text": "text"}
                                       )

    assert response_create_note.status_code == 201


def test_get_own_note(client: TestClient, auth_headers: dict):
    response_create_note = client.post("/notes",
                                       headers=auth_headers,
                                       json={"title": "title", "text": "text"}
                                       )

    note_id = response_create_note.json()["id"]

    response_get_note = client.get(f"/notes/{note_id}",
                                   headers=auth_headers
                                   )

    note = response_get_note.json()

    assert response_get_note.status_code == 200
    assert note["title"] == "title"


def test_get_another_users_note(client: TestClient, auth_headers: dict):
    response_create_note = client.post("/notes",
                                       headers=auth_headers,
                                       json={"title": "title", "text": "text"}
                                       )

    note_id = response_create_note.json()["id"]

    client.post("/register", json={"email": "user2@gmail.com", "password": "87654321"})
    response_other_user = client.post("/login", json={"email": "user2@gmail.com", "password": "87654321"})
    token = response_other_user.json()["access_token"]
    auth = {"Authorization": f"Bearer {token}"}

    response_get_another_users_note = client.get(f"/notes/{note_id}", headers=auth)

    assert response_get_another_users_note.status_code == 404


def test_return_own_notes(client: TestClient, auth_headers: dict):
    response_create_note1 = client.post("/notes", headers=auth_headers, json={"title": "title", "text": "text"})
    response_create_note2 = client.post("/notes", headers=auth_headers, json={"title": "title2", "text": "text2"})

    response_notes = client.get("/notes", headers=auth_headers)
    notes = response_notes.json()
    title1 = notes[0]["title"]
    title2 = notes[1]["title"]

    assert response_notes.status_code == 200
    assert len(notes) == 2
    assert title1 == "title"
    assert title2 == "title2"


def test_update(client: TestClient, auth_headers: dict):
    response_create_note = client.post("/notes", headers=auth_headers, json={"title": "title", "text": "text"})
    note_id = response_create_note.json()["id"]

    response_update_title = client.patch(f"/notes/{note_id}", headers=auth_headers, json={"title": "changed title"})
    response_update_text = client.patch(f"/notes/{note_id}", headers=auth_headers, json={"text": "changed text"})

    updated_title_note = response_update_title.json()
    updated_text_note = response_update_text.json()

    assert response_update_title.status_code == 200
    assert response_update_text.status_code == 200
    assert updated_title_note["title"] == "changed title"
    assert updated_text_note["text"] == "changed text"


def test_update_missing_id(client: TestClient, auth_headers: dict):
    response_update = client.patch("/notes/99999", headers=auth_headers, json={"title": "new title"})
    assert response_update.status_code == 404


def test_delete(client: TestClient, auth_headers: dict):
    response_create_note = client.post("/notes", headers=auth_headers, json={"title": "title", "text": "text"})
    note_id = response_create_note.json()["id"]

    response_delete_note = client.delete(f"/notes/{note_id}", headers=auth_headers)

    assert response_delete_note.status_code == 204


def test_create_with_empty_title(client: TestClient, auth_headers: dict):
    response_create_note = client.post("/notes", headers=auth_headers, json={"text": "text"})

    assert response_create_note.status_code == 422
