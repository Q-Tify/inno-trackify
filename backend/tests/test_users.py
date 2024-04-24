import unittest
from unittest.mock import Mock, patch

from sqlalchemy.orm import Session

from ..app import models
from ..app.schemas import users as schemas
from ..app.crud.users import get_users, get_user, get_user_by_email, get_user_by_username, validate_email, create_user, update_user, delete_user


class TestUserFunctions(unittest.TestCase):

    def setUp(self):
        self.db = Session()

    @patch('sqlalchemy.orm.Session.query')
    def test_get_users(self, mock_query):
        mock_query.return_value.all.return_value = []
        users = get_users(self.db)
        self.assertEqual(users, [])

    @patch('sqlalchemy.orm.Session.query')
    def test_get_user(self, mock_query):
        mock_query.return_value.filter.return_value.first.return_value = models.User(id=1, email="test@example.com", password="password", username="test")
        user = get_user(self.db, 1)
        self.assertEqual(user.id, 1)
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.password, "password")
        self.assertEqual(user.username, "test")

    @patch('sqlalchemy.orm.Session.query')
    def test_get_user_by_email(self, mock_query):
        mock_query.return_value.filter.return_value.first.return_value = models.User(id=1, email="test@example.com", password="password", username="test")
        user = get_user_by_email(self.db, "test@example.com")
        self.assertEqual(user.id, 1)
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.password, "password")
        self.assertEqual(user.username, "test")

    @patch('sqlalchemy.orm.Session.query')
    def test_get_user_by_username(self, mock_query):
        mock_query.return_value.filter.return_value.first.return_value = models.User(id=1, email="test@example.com", password="password", username="test")
        user = get_user_by_username(self.db, "test")
        self.assertEqual(user.id, 1)
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.password, "password")
        self.assertEqual(user.username, "test")

    def test_validate_email(self):
        self.assertTrue(validate_email("test@example.com"))
        self.assertFalse(validate_email("test"))

    @patch('sqlalchemy.orm.Session.add')
    @patch('sqlalchemy.orm.Session.commit')
    @patch('sqlalchemy.orm.Session.refresh')
    def test_create_user(self, mock_refresh, mock_commit, mock_add):
        user = schemas.UserCreate(email="test@example.com", password="password", username="test")
        created_user = create_user(self.db, user)
        self.assertEqual(created_user.email, "test@example.com")
        self.assertEqual(created_user.password, "password")
        self.assertEqual(created_user.username, "test")

    @patch('sqlalchemy.orm.Session.query')
    @patch('sqlalchemy.orm.Session.commit')
    @patch('sqlalchemy.orm.Session.refresh')
    def test_update_user(self, mock_refresh, mock_commit, mock_query):
        mock_query.return_value.filter.return_value.first.return_value = models.User(id=1, email="test@example.com", password="password", username="test")
        user = schemas.UserUpdate(email="new@example.com", password="new_password", username="new_username")
        updated_user = update_user(self.db, 1, user)
        self.assertEqual(updated_user.email, "new@example.com")
        self.assertEqual(updated_user.password, "new_password")
        self.assertEqual(updated_user.username, "new_username")
    
    @patch('sqlalchemy.orm.Session.query')
    @patch('sqlalchemy.orm.Session.commit')
    @patch('sqlalchemy.orm.Session.refresh')
    def test_update_user_none(self, mock_refresh, mock_commit, mock_query):
        mock_query.return_value.filter.return_value.first.return_value = None
        user = schemas.UserUpdate(email="new@example.com", password="new_password", username="new_username")
        updated_user = update_user(self.db, 1, user)
        self.assertEqual(updated_user, None)

    @patch('sqlalchemy.orm.Session.query')
    @patch('sqlalchemy.orm.Session.delete')
    @patch('sqlalchemy.orm.Session.commit')
    def test_delete_user(self, mock_commit, mock_delete, mock_query):
        mock_query.return_value.filter.return_value.first.return_value = models.User(id=1, email="test@example.com", password="password", username="test")
        response = delete_user(self.db, 1)
        self.assertEqual(response, {"message": "User deleted successfully"})

    @patch('sqlalchemy.orm.Session.query')
    @patch('sqlalchemy.orm.Session.delete')
    @patch('sqlalchemy.orm.Session.commit')
    def test_delete_user_not_found(self, mock_commit, mock_delete, mock_query):
        mock_query.return_value.filter.return_value.first.return_value = None
        response = delete_user(self.db, 1)
        self.assertEqual(response, {"message": "User not found"})
