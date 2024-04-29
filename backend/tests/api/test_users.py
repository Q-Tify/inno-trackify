import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch

from backend.app.api.authentication import authenticate_user
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
    with patch("backend.app.api.users.authenticate_user") as mock_authenticate_user:
        # Mock the return value of authenticate_user
        mock_authenticate_user.return_value = {"username": "test_user"}

        # Call the function with a valid token
        user = get_current_user(token=token, db=db_session)

        # Assertions
        assert user == {"username": "test_user"}


def test_get_current_user_unauthenticated(token, db_session):
    with patch("backend.app.api.users.authenticate_user") as mock_authenticate_user:
        # Mock the return value of authenticate_user to simulate authentication failure
        mock_authenticate_user.return_value = None

        # Call the function with an invalid token
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(token=token, db=db_session)

        # Assertions
        assert exc_info.value.status_code == HTTP_401_UNAUTHORIZED
        assert exc_info.value.detail == "Invalid authentication credentials"
        assert exc_info.value.headers == {"WWW-Authenticate": "Bearer"}


@pytest.fixture(autouse=True)
def mock_authenticate_user():
    with patch("backend.app.api.users.authenticate_user", MagicMock()) as mock_authenticate_user:
        yield mock_authenticate_user

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
        pass  # StopIteration will be raised when the generator is exhausted, meaning the session is closed
    else:
        assert False, "Generator should be exhausted after yielding the database session"

@patch("backend.app.api.users.authenticate_user")
@patch("backend.app.api.users.crud.get_users")
def test_get_users(mock_get_users, mock_authenticate_user, client, db_session):
    # Mock the return value of get_users to include the id field
    mock_get_users.return_value = [
        {"id": 1, "email": "lol1@example.com", "password": "password1", "username": "user1"},
        {"id": 2, "email": "lol2@example.com", "password": "password2", "username": "user2"},
    ]

    mock_authenticate_user.return_value = {"username": "test_user"}

    # Make the request to fetch all users
    response = client.get("/users/", headers={"Authorization": "Bearer valid_token"})

    # Assertions
    assert response.status_code == 200
    users = response.json()
    assert len(users) == 2
    assert users[0]["email"] == "lol1@example.com"
    assert users[1]["email"] == "lol2@example.com"

@patch("backend.app.api.users.authenticate_user")
@patch("backend.app.api.users.crud.get_user")
def test_get_user_found(mock_get_user, mock_authenticate_user, client, db_session):
    # Mock the return value of get_user including the "password" field
    mock_get_user.return_value = {"id": 1, "email": "test@example.com", "username": "test_user", "password": "dummy_password"}

    mock_authenticate_user.return_value = {"username": "test_user"}
    # Make the request to fetch a user by ID 1
    response = client.get("/users/1", headers={"Authorization": "Bearer valid_token"})

    # Assertions
    assert response.status_code == 200
    user = response.json()
    assert user["id"] == 1
    assert user["email"] == "test@example.com"
    assert user["username"] == "test_user"

@patch("backend.app.api.users.authenticate_user")
@patch("backend.app.api.users.crud.get_user")
def test_get_user_not_found(mock_get_user, mock_authenticate_user, client, db_session):
    # Mock the return value of get_user to simulate user not found
    mock_get_user.return_value = None

    mock_authenticate_user.return_value = {"username": "test_user"}

    with pytest.raises(HTTPException) as exc_info:
        client.get("/users/2", headers={"Authorization": "Bearer valid_token"})

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User not found"

@patch("backend.app.api.users.crud.validate_email")
def test_create_user_valid_email(mock_validate_email, client, db_session):
    # Mocking the return value of validate_email function
    mock_validate_email.return_value = True

    # Making the request to create a new user
    user_create_data = {"email": "test_create_user_valid_email@example.com", "password": "password123", "username": "test_user"}
    response = client.post("/users/", json=user_create_data)

    # Assertions
    assert response.status_code == 200
    assert response.json()["email"] == user_create_data["email"]
    assert response.json()["username"] == user_create_data["username"]

@patch("backend.app.api.users.crud.validate_email")
def test_create_user_invalid_email(mock_validate_email, client, db_session):
    # Mocking the return value of validate_email function
    mock_validate_email.return_value = False

    # Making the request to create a new user with an invalid email
    user_create_data = {"email": "invalid-email", "password": "password123", "username": "test_user"}
    with pytest.raises(HTTPException) as exc_info:
        client.post("/users/", json=user_create_data)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Invalid email address"

@patch("backend.app.api.users.authenticate_user")
@patch("backend.app.api.users.crud.update_user")
def test_update_user(mock_update_user, mock_authenticate_user, client, db_session):
    # Mock the return value of update_user
    mock_update_user.return_value = {"id": 1, "email": "updated@example.com", "username": "updated_user", "password": "dummy_password"}

    mock_authenticate_user.return_value = {"username": "updated_user"}

    # Make the request to update an existing user
    user_update_data = {"email": "updated@example.com", "username": "updated_user", "password": "dummy_password"}
    response = client.put("/users/1", json=user_update_data, headers={"Authorization": "Bearer valid_token"})

    # Assertions
    assert response.status_code == 200
    updated_user = response.json()
    assert updated_user["id"] == 1
    assert updated_user["email"] == "updated@example.com"
    assert updated_user["username"] == "updated_user"


@patch("backend.app.api.users.authenticate_user")
@patch("backend.app.api.users.crud.delete_user")
def test_delete_user(mock_delete_user, mock_authenticate_user, client, db_session):
    # Mock the return value of authenticate_user
    mock_authenticate_user.return_value = {"username": "test_user"}

    # Mock the return value of delete_user
    mock_delete_user.return_value = None

    # Make the request to delete a user
    response = client.delete("/users/1", headers={"Authorization": "Bearer valid_token"})

    # Assertions
    assert response.status_code == 200

