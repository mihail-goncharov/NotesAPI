# Notes API

A REST API where authenticated users can create, read, update, and delete their own personal notes.

Built as a learning project to work through the full backend stack end to end — from request validation and database modelling to JWT authentication and per-user data isolation.

## Stack

| Area | Choice |
|---|---|
| Language | Python 3.12 |
| Framework | FastAPI |
| Validation | Pydantic v2 |
| Database | PostgreSQL |
| ORM | SQLAlchemy 2.x |
| Auth | JWT (PyJWT), Argon2 password hashing (pwdlib) |
| Server | Uvicorn |
| Testing | pytest, FastAPI TestClient |

## Features

- **Authentication** — registration, login, and JWT-based session handling
- **Password security** — Argon2 hashing via `pwdlib`; plaintext passwords are never stored or returned
- **Per-user data isolation** — every note is owned by a user; one user cannot read, update, or delete another user's notes
- **Full CRUD** — create, list, fetch, partially update, and delete notes
- **Validation** — request/response schemas with length and value constraints, enforced by Pydantic
- **Pagination** — `offset`/`limit` query parameters with bounds checking
- **Per-user title uniqueness** — enforced both in application logic and by a composite database constraint

## Architecture

The app is organised in layers, each with a single responsibility:

```
app/
  main.py            # entry point, lifespan hook, router registration
  database/
    session.py       # engine, session dependency, env validation
  models/            # SQLAlchemy models (database tables)
    base.py
    user.py
    note.py
  schemas/           # Pydantic models (API request/response contracts)
    user.py
    note.py
  routers/           # HTTP endpoints
    auth.py
    note.py
  services/          # business logic
    auth.py          # hashing, JWT creation, current-user resolution
  testing/           # pytest suite
    conftest.py      # shared fixtures: isolated test DB, client, auth headers
    test_auth.py
    test_note.py
```

`models/` and `schemas/` are deliberately separate: the shape of a database row and the shape of an API payload are not the same thing. For example, `user_id` exists on the `Note` table but never appears in a note-creation request — the server derives it from the authenticated user, so a client cannot claim ownership of someone else's data.

## Setup

**Requirements:** Python 3.12+, PostgreSQL 17

```bash
# 1. Clone and enter the project
git clone https://github.com/mihail-goncharov/NotesAPI.git
cd NotesAPI

# 2. Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create a database in PostgreSQL
#    (via psql, pgAdmin, or your tool of choice)
createdb notesapi

# 5. Configure environment variables
copy .env.example .env        # Windows
# cp .env.example .env        # macOS / Linux
```

Then open `.env` and fill in your real values:

```
DATABASE_URL=postgresql+psycopg2://username:password@localhost:5432/notesapi
SECRET_KEY=<generate one, see below>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL_TEST=postgresql+psycopg2://username:password@localhost:5432/notesapi_test
```

`DATABASE_URL_TEST` is only needed if you plan to run the test suite (see below).

Generate a signing secret:

```bash
openssl rand -hex 32
```

The app validates all required environment variables at startup and fails immediately with a clear message if any are missing.

## Running

```bash
fastapi dev
```

Tables are created automatically on startup. The API is then available at `http://127.0.0.1:8000`, with interactive documentation at `http://127.0.0.1:8000/docs`.

## Running tests

Tests run against a separate, disposable database — never against your development data. Each test gets a fresh set of tables, created before it runs and dropped after.

```bash
# 1. Create a second database for tests
createdb notesapi_test

# 2. Set DATABASE_URL_TEST in .env (see Setup above)

# 3. Run the suite
pytest
```

Coverage includes registration, login, authentication failures, full note CRUD, validation, and cross-user ownership checks. Not yet exhaustive — pagination bounds and additional edge cases are natural next additions.

## Endpoints

| Method | Path | Auth | Description |
|---|---|---|---|
| `POST` | `/register` | — | Create an account |
| `POST` | `/login` | — | Authenticate, receive a JWT |
| `POST` | `/token` | — | OAuth2 form login (used by the Swagger UI "Authorize" button) |
| `POST` | `/notes` | ✓ | Create a note |
| `GET` | `/notes` | ✓ | List your notes (`offset`, `limit`) |
| `GET` | `/notes/{note_id}` | ✓ | Fetch one of your notes |
| `PATCH` | `/notes/{note_id}` | ✓ | Partially update a note |
| `DELETE` | `/notes/{note_id}` | ✓ | Delete a note |

Protected endpoints expect an `Authorization: Bearer <token>` header. In the Swagger UI, click **Authorize** and log in — the header is then attached automatically.

### Error semantics

| Code | Meaning |
|---|---|
| `401` | Missing, malformed, or expired token; failed login |
| `404` | Note not found — also returned for notes belonging to another user, so the API never confirms whether a given note exists |
| `409` | Email already registered, or a note with that title already exists for this user |
| `422` | Request failed schema validation |

Login failures return the same message whether the email is unknown or the password is wrong, so the API cannot be used to discover which addresses are registered.

## Known limitations

Deliberately out of scope for this version, listed here rather than left as silent gaps:

- **No migrations** — tables are created via SQLAlchemy's `create_all()`; Alembic is planned, which is what schema changes on live data actually require
- **Tags and search** were scoped out of the MVP
