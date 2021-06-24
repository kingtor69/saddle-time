import os
from unittest import TestCase
from models import db, User, Route, Checkpoint
from datetime import datetime

os.environ['DATABASE_URL'] = "postgresql:///saddle_time_test_db"

from app import app

db.drop_all()
db.create_all()

# TODO: this fails when I run the whole file, but if I do one test at a time, they all pass. I suspect this has something to do with setUp (and maybe should be doing something else on tearDown?)

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
         - exist (test will fail if user id was not created)
         - have a hashed password, which is to day:
            - password in the database should not equal the entered password
            - hashed password should have a length of 60 characters
            - all Bcrypt strings start with '$2b$' which should be true of the hashed password
            - if not specified, the default_bike_type should be "regular"
        """
        u = User.hashpass("test_user", "UNHASHED_PASSWORD")
        db.session.add(u)
        db.session.commit()

        self.assertTrue(u.id)
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
        cp = Checkpoint(route_id=r1.id, x=1, point_x_lat=35.174078, point_x_lng=-106.55891)
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
        cp1 = Checkpoint(route_id=r2.id, x=1, point_x_lat=35.174078, point_x_lng=-106.55891)
        cp2 = Checkpoint(route_id=r2.id, x=2, point_x_lat=35.132659, point_x_lng=-106.49771)
        cp3 = Checkpoint(route_id=r3.id, x=1, point_x_lat=35.174078, point_x_lng=-106.55891)
        db.session.add_all([cp1, cp2, cp3])
        db.session.commit()
        u_id = u.id
        # guest_id = guest.id
        r1_id = r1.id
        r2_id = r2.id
        r3_id = r3.id
        # cp1_pk = (cp1.route_id, cp1.x)
        # cp2_pk = (cp2.route_id, cp2.x)
        cp3_pk = (cp3.route_id, cp3.x)
        test_r3 = make_test_route(r3_id)
        test_cp3 = make_test_checkpoint(cp3_pk, r2_id)
        # nothing deleted yet, so tests cases should correspond to input
        self.assertEqual(test_r3.id, r3_id)
        self.assertEqual((test_cp3.route_id, test_cp3.x), cp3_pk)
        db.session.delete(u)
        db.session.delete(r3)
        db.session.delete(cp2)
        db.session.commit()
        test_cascade_r3 = make_test_route(r3_id)
        test_cascade_cp3 = make_test_checkpoint(cp3_pk, r2_id)
        test_cascade_r2 = make_test_route(r2_id)
        # inputs to test cases have been deleted, so test cases should NOT correspond to input 
        self.assertNotEqual(test_cascade_r3.id, r3_id)
        self.assertNotEqual((test_cascade_cp3.route_id, test_cascade_cp3.x), cp3_pk)
        # but route corresponding to deleted checkpoint should still correspond to input
        self.assertEqual(test_cascade_r2.id, r2_id)






def users_and_route_setup(timestamp):
    """Set up testing data:
    1 generic user, 1 guest user
    3 routes (1 with defaults, 1 with customized data, 1 with a mixture)
    (argument timestamp is used for routes)
    return a tuple of those 5 ORMs in that order
    """
    u = User.hashpass("test_user", "UNHASHED_PASSWORD")
    guest = User.hashpass("guest_user", "guestPassw0rd!")
    guest.default_bike_type = "road"
    db.session.add_all([u, guest])
    db.session.commit()
    r1 = Route(start_lat=35.190564, start_lng=-106.580526, end_lat=35.11882, end_lng=-106.71952, timestamp=timestamp, user_id=u.id)
    r2 = Route(start_display_name="work", start_lat=35.190564, start_lng=-106.580526, end_display_name="rink", end_lat=35.11882, end_lng=-106.71952, bike_type="mountain", route_name="go play hockey", timestamp=timestamp, user_id=guest.id)
    r3 = Route(start_lat=35.190564, start_lng=-106.580526, end_lat=35.11882, end_lng=-106.71952, route_name="go play hockey", timestamp=timestamp, user_id=guest.id)
    db.session.add_all([r1, r2, r3])
    db.session.commit()
    return (u, guest, r1, r2, r3)
    
def make_test_route(id):
    test_route = Route.query.filter_by(id=id).first()
    if not test_route:
        test_route=Route(start_lat=51.484186, start_lng=0.004834, end_lat=-33.928905, end_lng=-33.928905)
        db.session.add(test_route)
        db.session.commit()
    return test_route

def make_test_checkpoint(pk, rid):
    (route_id, x) = pk
    test_checkpoint = Checkpoint.query.get((route_id, x))
    if not test_checkpoint:
        test_checkpoint = Checkpoint(route_id=rid, x=2, point_x_lat=-33.928905, point_x_lng=18.417249)
        db.session.add(test_checkpoint)
        db.session.commit()
    return test_checkpoint
