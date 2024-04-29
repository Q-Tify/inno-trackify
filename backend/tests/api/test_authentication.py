import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from backend.app.api.authentication import router, get_db
from backend.app.api.authentication import authenticate_user
from sqlalchemy.orm import Session
from fastapi import HTTPException

@pytest.fixture
def client():
    return TestClient(router)


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


@patch("backend.app.api.authentication.crud_auth.get_user_username_password")
def test_create_access_token_valid_user(mock_get_user, client):
    # Mocking the user object returned by get_user_username_password
    mock_user = MagicMock()
    mock_user.username = "testuser"
    mock_get_user.return_value = mock_user

    response = client.post("/login", data={"username": "testuser", "password": "testpass"}) ##NOSONAR
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


@patch("backend.app.api.authentication.crud_auth.get_user_username_password")
def test_create_access_token_invalid_user(mock_get_user, client):
    # Mocking return value for invalid user
    mock_get_user.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        client.post("/login", data={"username": "invalid", "password": "invalid"}) ##NOSONAR

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Incorrect username or password"

def test_authenticate_user_valid_token():
    # Mocking dependencies and database session
    db_mock = MagicMock(spec=Session)
    token = "valid_token"
    username = "test_user"

    # Mocking get_username_from_token to return a valid username
    with patch("backend.app.api.authentication.crud_auth.get_username_from_token") as mock_get_username:
        mock_get_username.return_value = username

        # Mocking get_user_by_username to return a user object
        with patch("backend.app.api.authentication.crud_users.get_user_by_username") as mock_get_user:
            user_mock = MagicMock()
            mock_get_user.return_value = user_mock

            # Call the authenticate_user function
            result = authenticate_user(db_mock, token)

            # Assertions
            assert result == user_mock
            mock_get_username.assert_called_once_with(token)
            mock_get_user.assert_called_once_with(db_mock, username)

def test_authenticate_user_invalid_token():
    # Mocking dependencies and database session
    db_mock = MagicMock(spec=Session)
    token = "invalid_token"

    # Mocking get_username_from_token to return None (invalid token)
    with patch("backend.app.api.authentication.crud_auth.get_username_from_token") as mock_get_username:
        mock_get_username.return_value = None

        # Call the authenticate_user function
        result = authenticate_user(db_mock, token)

        # Assertions
        assert result is None
        mock_get_username.assert_called_once_with(token)

def test_authenticate_user_exception():
    # Mocking dependencies and database session
    db_mock = MagicMock(spec=Session)
    token = "valid_token"

    # Mocking get_username_from_token to raise an exception
    with patch("backend.app.api.authentication.crud_auth.get_username_from_token") as mock_get_username:
        mock_get_username.side_effect = Exception("An error occurred")

        # Call the authenticate_user function
        result = authenticate_user(db_mock, token)

        # Assertions
        assert result is None
        mock_get_username.assert_called_once_with(token)

