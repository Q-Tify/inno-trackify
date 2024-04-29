import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from backend.app.api.users import get_current_user
from backend.app.api.users import router, get_db
from starlette.status import HTTP_401_UNAUTHORIZED
from sqlalchemy.orm import Session
from backend.app.models import Base
from backend.app.database import engine
from fastapi import HTTPException


Base.metadata.create_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(router)


@pytest.fixture
def db_session():
    session = Session(bind=engine)
    try:
        yield session
    finally:
        session.rollback()  # Rollback changes after each test
        session.close()  # Close the session


@pytest.fixture
def token():
    return "valid_token"


def test_get_current_user_authenticated(token, db_session):
    with patch(
        "backend.app.api.users.authenticate_user"
    ) as mock_authenticate_user:
        # Mock the return value of authenticate_user
        mock_authenticate_user.return_value = {"username": "test_user"}

        # Call the function with a valid token
        user = get_current_user(token=token, db=db_session)

        # Assertions
        assert user == {"username": "test_user"}


def test_get_current_user_unauthenticated(token, db_session):
    with patch(
        "backend.app.api.users.authenticate_user"
    ) as mock_authenticate_user:
        mock_authenticate_user.return_value = None

        # Call the function with an invalid token
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(token=token, db=db_session)

        # Assertions
        assert exc_info.value.status_code == HTTP_401_UNAUTHORIZED
        assert exc_info.value.detail == "Invalid authentication credentials"
        assert exc_info.value.headers == {"WWW-Authenticate": "Bearer"}


def test_get_db():
    # Call the get_db function to get the generator
    db_gen = get_db()
    # Get the database session by calling next() on the generator
    db = next(db_gen)
    # Assertions
    assert db is not None  # Check if the database session is created
    # Ensure that the session is closed after yielding
    try:
        next(db_gen)  # Attempt to get the next item from the generator
    except StopIteration:
        pass
    else:
        assert (
            False
        ), "Generator should be exhausted after yielding the database session"
