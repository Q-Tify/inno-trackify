import unittest
from unittest.mock import patch

from sqlalchemy.orm import Session

from ..app import models
from ..app.schemas import activities as schemas
from ..app.crud.activities import get_activities, get_activity, update_activity,delete_activity, create_activity

class TestActivityFunctions(unittest.TestCase):

    def setUp(self):
        self.db = Session()

    @patch('sqlalchemy.orm.Session.query')
    def test_get_activities(self, mock_query):
        mock_query.return_value.all.return_value = []
        activities = get_activities(self.db)
        self.assertEqual(activities, [])

    @patch('sqlalchemy.orm.Session.query')
    def test_get_activity(self, mock_query):
        mock_query.return_value.filter.return_value.first.return_value = models.Activity(id=1, name="test activity", description="test description")
        activity = get_activity(self.db, 1)
        self.assertEqual(activity.id, 1)
        self.assertEqual(activity.name, "test activity")
        self.assertEqual(activity.description, "test description")

    @patch('sqlalchemy.orm.Session.add')
    @patch('sqlalchemy.orm.Session.commit')
    @patch('sqlalchemy.orm.Session.refresh')
    def test_create_activity(self, mock_refresh, mock_commit, mock_add):
        activity = schemas.ActivityCreate(name="test activity", description="test description", type_id = 1,
                                          user_id=2, start_time="12:30", end_time="14:00", duration="1:30")
        created_activity = create_activity(self.db, activity)
        self.assertEqual(created_activity.name, "test activity")
        self.assertEqual(created_activity.description, "test description")

    @patch('sqlalchemy.orm.Session.query')
    @patch('sqlalchemy.orm.Session.commit')
    @patch('sqlalchemy.orm.Session.refresh')
    def test_update_activity(self, mock_refresh, mock_commit, mock_query):
        mock_query.return_value.filter.return_value.first.return_value = models.Activity(id=1, name="test activity", description="test description", type_id=1)
        activity = schemas.ActivityUpdate(name="new test activity", description="new test description", type_id=1)
        updated_activity = update_activity(self.db, 1, activity)
        self.assertEqual(updated_activity.id, 1)
        # self.assertEqual(updated_activity.name, "new test activity")
        # self.assertEqual(updated_activity.description, "new test description")
    
    @patch('sqlalchemy.orm.Session.query')
    @patch('sqlalchemy.orm.Session.commit')
    @patch('sqlalchemy.orm.Session.refresh')
    def test_update_activity_none(self, mock_refresh, mock_commit, mock_query):
        mock_query.return_value.filter.return_value.first.return_value = None
        activity = schemas.ActivityUpdate(name="new test activity", description="new test description", type_id=1)
        updated_activity = update_activity(self.db, 1, activity)
        self.assertEqual(updated_activity, None)

    @patch('sqlalchemy.orm.Session.query')
    @patch('sqlalchemy.orm.Session.delete')
    @patch('sqlalchemy.orm.Session.commit')
    def test_delete_activity(self, mock_commit, mock_delete, mock_query):
        mock_query.return_value.filter.return_value.first.return_value = models.Activity(id=1, name="test activity", description="test description")
        response = delete_activity(self.db, 1)
        self.assertEqual(response, {"message": "Activity deleted successfully"})

    @patch('sqlalchemy.orm.Session.query')
    @patch('sqlalchemy.orm.Session.delete')
    @patch('sqlalchemy.orm.Session.commit')
    def test_delete_activity_not_found(self, mock_commit, mock_delete, mock_query):
        mock_query.return_value.filter.return_value.first.return_value = None
        response = delete_activity(self.db, 1)
        self.assertEqual(response, {"message": "Activity not found"})
