import unittest
from unittest.mock import patch
import bcrypt
import base64
from sqlalchemy.orm import Session

from backend.app import models
from datetime import datetime, timedelta, timezone
from jose import jwt
from backend.app.crud.authentication import (
    SECRET_KEY,
    get_user_username_password,
    get_username_from_token,
    create_access_token,
    ALGORITHM,
    EXPIRE_TIME_MINUTES,
)


class TestAuthenticationFunctions(unittest.TestCase):

    def setUp(self):
        self.db = Session()

    @patch("sqlalchemy.orm.Session.query")
    def test_get_user_username_password(self, mock_query):
        mock_query.return_value.filter.return_value.first.return_value = (
            models.User(id=1, username="test_user", password="test_password")
        )
        user = get_user_username_password(
            self.db, "test_user", "test_password"
        )
        self.assertEqual(user.id, 1)
        self.assertEqual(user.username, "test_user")
        self.assertEqual(user.password, "test_password")

    def test_create_access_token__expires(self):
        data = {"username": "test_user"}
        expires_delta = timedelta(minutes=EXPIRE_TIME_MINUTES)
        token = create_access_token(data, expires_delta)
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        self.assertEqual(decoded_token.get("username"), "test_user")
        self.assertTrue(
            datetime.now(timezone.utc) < datetime.fromtimestamp(decoded_token["exp"], timezone.utc)
        )

    def test_create_access_token__expires_default(self):
        data = {"username": "test_user"}
        token = create_access_token(data)
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        self.assertEqual(decoded_token.get("username"), "test_user")

    def test_get_username_from_token(self):
        data = {"sub": "test_user"}
        token = create_access_token(data)
        username = get_username_from_token(token)
        self.assertEqual(username, "test_user")
