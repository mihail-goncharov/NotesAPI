import os

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from database.session import get_session
from main import app
from models.base import Base

load_dotenv()

DB_URI_TEST = os.getenv("DATABASE_URL_TEST")


@pytest.fixture(name="session")
def session_fixture():
    test_engine = create_engine(DB_URI_TEST)
    Base.metadata.create_all(test_engine)
    with Session(test_engine) as session:
        yield session

    Base.metadata.drop_all(test_engine)


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="auth_headers")
def auth_headers_fixture(client: TestClient, session: Session):
    client.post("/register", json={"email": "user@gmail.com", "password": "123456789"})
    response = client.post("/login", json={"email": "user@gmail.com", "password": "123456789"})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
