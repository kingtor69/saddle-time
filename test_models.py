import os
from unittest import TestCase
from models import db, User, Route, Checkpoint
from datetime import datetime
from secrets import guest_pass

os.environ['DATABASE_URL'] = "postgresql:///saddle_time_test_db"

from app import app

db.create_all()

# TODO: this fails when I run the whole file, but if I do one test at a time, they all pass. I suspect this has something to do with setUp and/or tearDown and/or cascading behavior

class UserModelTestCase(TestCase):
    """Test User model."""

    def setUp(self):
        """Clear any leftover data,
        add testing data,
        create test client.
        """

        Route.query.delete()
        # TODO: putting Route first here is a kluge for the cascade not working in models.py. Fix that.
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
            - if not specified, the default_bike_type should be "regular"
        """
        u = User.hashpass("test_user", "UNHASHED_PASSWORD")
        db.session.add(u)
        db.session.commit()

        self.assertNotEqual(u.password, "UNHASHED_PASSWORD")
        self.assertEqual(len(u.password), 60)
        self.assertTrue(u.password.startswith("$2b$"))
        self.assertEqual(u.default_bike_type, "regular")

class RouteModelTestCase(TestCase):
    """test basic Route model"""
    
    def setUp(self):
        """Clear any leftover data,
        add testing data,
        create test client.
        """

        Route.query.delete()
        User.query.delete()

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
            - show a bike_type for the route:
                - if none is entered and user has none set, result should be "regular"
                - if none is entered and user has one set, result should be the user's default
                - if one is entered into route, that should be the result
            - have a timestamp to be used for reloading routes from API after 1 week
            - be associated with a user who created the route (can be guest user in app, will test both here)
        """
        ts = datetime.utcnow()
        (u, guest, r1, r2, r3) = users_and_route_setup(ts)

        self.assertEqual(r1.route_name, "untitled")
        self.assertEqual(r2.route_name, "go play hockey")
        self.assertEqual(r1.bike_type, "regular")
        self.assertEqual(r2.bike_type, "mountain")
        # TODO: write the logic for this - classmethod?
        # self.assertEqual(r3.bike_type, "road")
        self.assertTrue(r1.start_lat >= -180)
        self.assertTrue(r1.start_lat <= 180)
        self.assertTrue(r1.start_lng >= -180)
        self.assertTrue(r1.start_lng <= 180)
        self.assertTrue(r1.end_lat >= -180)
        self.assertTrue(r1.end_lat <= 180)
        self.assertTrue(r1.end_lng >= -180)
        self.assertTrue(r1.end_lng <= 180)
        self.assertEqual(r1.timestamp, ts)
        self.assertEqual(r1.user_id, u.id)
        self.assertEqual(r2.user_id, guest.id)
        
class CheckpointModelTestCase(TestCase):
    """test Checkpoint model"""

    def setUp(self):
        """Clear any leftover data,
        add testing data,
        create test client.
        """

        Checkpoint.query.delete()
        Route.query.delete()
        User.query.delete()

        self.client = app.test_client()

    def tearDown(self):
        """clear away any mess left by failed tests"""
        db.session.rollback()

    def test_checkpoint_model(self):
        """Test Checkpoint model
        A new checkpoint should:
         - have one new geolocation (lat and lng)
         - have a number to keep track of where it is in the route
         - refer to a route
        """
        ts = datetime.utcnow()
        (u, guest, r1, r2, r3) = users_and_route_setup(ts)
        cp = Checkpoint(route_id=r1.id, point_x_lat=35.174078, point_x_lng=-106.55891)
        db.session.add(cp)
        db.session.commit()
        
        self.assertTrue(cp.point_x_lat <= 180)
        self.assertTrue(cp.point_x_lat >= -180)
        self.assertTrue(cp.point_x_lng <= 180)
        self.assertTrue(cp.point_x_lng >= -180)
        self.assertTrue(type(cp.x) == int)
        self.assertEqual(cp.route_id, r1.id)

class CascadeTestCase(TestCase):
    """test all cascades"""

    def setUp(self):
        """Clear any leftover data,
        add testing data,
        create test client.
        """

        Checkpoint.query.delete()
        Route.query.delete()
        User.query.delete()

        self.client = app.test_client()

    def tearDown(self):
        """clear away any mess left by failed tests"""
        db.session.rollback()

    def test_cascades(self):
        """test cascade behavior for all models
            - when a user is deleted, all routes associated with that user should be deleted
            - when a route is deleted, all checkpoints associated with that route should be deleted
            - when a checkpoint is deleted, the route should stay intact
        """
        ts = datetime.utcnow()
        (u, guest, r1, r2, r3) = users_and_route_setup(ts)
        
        




def users_and_route_setup(timestamp):
    """Set up testing data:
    1 generic user, 1 guest user
    3 routes (1 with defaults, 1 with customized data, 1 with a mixture)
    (argument timestamp is used for routes)
    return a tuple of those 5 ORMs in that order
    """
    u = User.hashpass("test_user", "UNHASHED_PASSWORD")
    guest = User.hashpass("guest_user", guest_pass)
    guest.default_bike_type = "road"
    db.session.add_all([u, guest])
    db.session.commit()
    r1 = Route(start_lat=35.190564, start_lng=-106.580526, end_lat=35.11882, end_lng=-106.71952, timestamp=timestamp, user_id=u.id)
    r2 = Route(start_lat=35.190564, start_lng=-106.580526, end_lat=35.11882, end_lng=-106.71952, bike_type="mountain", route_name="go play hockey", timestamp=timestamp, user_id=guest.id)
    r3 = Route(start_lat=35.190564, start_lng=-106.580526, end_lat=35.11882, end_lng=-106.71952, route_name="go play hockey", timestamp=timestamp, user_id=guest.id)
    db.session.add_all([r1, r2, r3])
    db.session.commit()
    return (u, guest, r1, r2, r3)
    