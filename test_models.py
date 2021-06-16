import os
from unittest import TestCase
from models import db, User, Route, Checkpoint
from datetime import datetime
from secrets import guest_pass

os.environ['DATABASE_URL'] = "postgresql:///saddle_time_test_db"

from app import app

db.create_all()

class UserModelTestCase(TestCase):
    """Test User model."""

    def setUp(self):
        """Clear any leftover data,
        add testing data,
        create test client.
        """

        User.query.delete()

        self.client = app.test_client()

    def tearDown(self):
        """clear away any mess left by failed tests"""
        db.session.rollback()

    def test_user_model(self):
        """Does the basic User model work?
        A new user should:
         - exist (test will fail if user was not created)
         - have a hashed password, which is to day:
            - password in the database should not equal the entered password
            - hashed password should have a length of 60 characters
            - all Bcrypt strings start with '$2b$' which should be true of the hashed password
        """
        u = User.hashpass("test_user", "UNHASHED_PASSWORD")
        db.session.add(u)
        db.session.commit()

        self.assertNotEqual(u.password, "UNHASHED_PASSWORD")
        self.assertEqual(len(u.password), 60)
        self.assertTrue(u.password.startswith("$2b$"))

class RouteModelTestCase(TestCase):
    """test basic Route model"""
    
    def setUp(self):
        """Clear any leftover data,
        add testing data,
        create test client.
        """

        User.query.delete()
        Route.query.delete()

        self.client = app.test_client()

    def tearDown(self):
        """clear away any mess left by failed tests"""
        db.session.rollback()


    def test_route_model(self):
        """does the Route model work?
        A new route should:
            - exist
            - contain a route_name, whether it be default or entered
            - have start and end latitues and longitutes between -180 and 180
            # TODO: that test should use an API call, but I don't think that should be in the models tests because it's going to be a flask operation
            - show a bike_type for the route (again, default or entered)
            - have a timestamp to be used for reloading routes from API after 1 week
            - be associated with a user who created the route (can be guest user in app, will test both here)
        """
        ts = datetime.utcnow()
        u = User.hashpass("test_user", "UNHASHED_PASSWORD")
        r_defaults = Route(start_lat=35.190564, start_lng=-106.580526, end_lat=35.11882, end_lng=-106.71952, timestamp=ts, user_id=u.id)
        guest = User.hashpass("guest_user", guest_pass)
        r_custom = Route(start_lat=35.190564, start_lng=-106.580526, end_lat=35.11882, end_lng=-106.71952, bike_type="road", route_name="go play hockey", timestamp=ts, user_id=guest.id)

        self.assertEqual(r_defaults.route_name, "untitled")
        self.assertEqual(r_custom.route_name, "go play hockey")
        self.assertEqual(r_defaults.bike_type, "regular")
        self.assertEqual(r_custom.bike_type, "road")
        self.assertTrue(r_defaults.start_lat >= -180)
        self.assertTrue(r_defaults.start_lat <= 180)
        self.assertTrue(r_defaults.start_lng >= -180)
        self.assertTrue(r_defaults.start_lng <= 180)
        self.assertTrue(r_defaults.end_lat >= -180)
        self.assertTrue(r_defaults.end_lat <= 180)
        self.assertTrue(r_defaults.end_lng >= -180)
        self.assertTrue(r_defaults.end_lng <= 180)
        self.assertEqual(r_defaults.timestamp, ts)
        self.assertEqual(r_defaults.user_id, u.id)
        self.assertEqual(r_custom.user_id, guest.id)
        
