import os
from unittest import TestCase
from models import db, User, Route, Checkpoint, CheckpointRoute
from datetime import datetime

os.environ['DATABASE_URL'] = "postgresql:///saddle_time_test_db"

from app import app

db.drop_all()
db.create_all()

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
        u1 = User.hashpass("test_user", "UNHASHED_PASSWORD")
        u1.email = "email@notreally.com"
        db.session.add(u1)
        db.session.commit()

        self.assertTrue(u1.id)
        self.assertNotEqual(u1.password, "UNHASHED_PASSWORD")
        self.assertEqual(len(u1.password), 60)
        self.assertTrue(u1.password.startswith("$2b$"))
        self.assertEqual(u1.default_bike_type, "regular")

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
            # TODO: that test should use an API call, but I don't think that should be in the models tests because it's going to be a flask operation
            - show a bike_type for the route:
                - if none is entered and user has none set, result should be "regular"
                - if none is entered and user has one set, result should be the user's default
                - if one is entered into route, that should be the result
            - have a timestamp to be used for reloading routes from API after a fortnight
            - be associated with a user who created the route 
        """
        ts = datetime.utcnow()
        (u1, u2) = user_setups_for_tests()
        (r1, r2, r3) = route_setups_for_tests(ts, u1, u2)

        self.assertEqual(r1.route_name, "untitled")
        self.assertEqual(r2.route_name, "go play hockey")
        self.assertEqual(r1.bike_type, "regular")
        self.assertEqual(r2.bike_type, "mountain")
        # TODO: write the logic for this - classmethod?
        # self.assertEqual(r3.bike_type, "road")
        self.assertEqual(r1.timestamp, ts)
        self.assertEqual(r1.user_id, u1.id)
        self.assertEqual(r2.user_id, u2.id)
        
class CheckpointModelTestCase(TestCase):
    """test Checkpoint model"""
    def setUp(self):
        """Clear any leftover data,
        add testing data,
        create test client.
        """

        Checkpoint.query.delete()
        User.query.delete()

        self.client = app.test_client()

    def tearDown(self):
        """clear away any mess left by failed tests"""
        db.session.rollback()

    def test_checkpoint_model(self):
        """Test Checkpoint model
            a new checkpoint should:
             - exist
             - have lattitude and longitude entries in the range of -180 to 180
             - be linked to a valid user
        """
        ts = datetime.utcnow()
        (u1, u2) = user_setups_for_tests()
        cps = checkpoint_setups_for_tests(u1, u2)
        db.session.add_all(cps)
        db.session.commit()
        
        for i in range(len(cps)):
            self.assertTrue(cps[i].checkpoint_lat <= 180)
            self.assertTrue(cps[i].checkpoint_lat >= -180)
            self.assertTrue(cps[i].checkpoint_lng <= 180)
            self.assertTrue(cps[i].checkpoint_lng >= -180)
            if i < 4:
                self.assertEqual(cps[i].user_id, u1.id)
            else:
                self.assertEqual(cps[i].user_id, u2.id)

class CheckpointRouteTestCase(TestCase):
    """test route-checkpoints model"""
    def setUp(self):
        """Clear any leftover data,
        add testing data,
        create test client.
        """

        CheckpointRoute.query.delete()
        Checkpoint.query.delete()
        Route.query.delete()
        User.query.delete()

        self.client = app.test_client()

    def tearDown(self):
        """clear away any mess left by failed tests"""
        db.session.rollback()

    def test_checkpoint_routes(self):
        """a new route-checkpoint entry should:
            - exist
            - be linked to a route and a checkpoint
            - have an order for which checkpoint it is in a route     
        """
        ts = datetime.utcnow()
        (u1, u2) = user_setups_for_tests()
        (r1, r2, r3) = route_setups_for_tests(ts, u1, u2)
        

####################################3
# methods to set up test data
def user_setups_for_tests():
    """Set up testing data:
    2 users
    (argument timestamp is used for routes)
    return a tuple of those 2 ORMs in that order
    """
    u1 = User.hashpass("test_user", "UNHASHED_PASSWORD")
    u1.email = "email@nope.com"
    u2 = User.hashpass("u2_user", "u2Passw0rd!")
    u2.email = "ilike@bananas.com"
    u2.default_bike_type = "road"
    db.session.add_all([u1, u2])
    db.session.commit()
    return (u1, u2)

def route_setups_for_tests(timestamp, u1, u2):
    """Set up testing data:
    3 routes (1 with defaults, 1 with customized data, 1 with a mixture)
    linked to users entered as arguments
    return a tuple of those 3 ORMs in that order

    """
    r1 = Route(timestamp=timestamp, user_id=u1.id)
    r2 = Route(bike_type="mountain", route_name="go play hockey", timestamp=timestamp, user_id=u2.id)
    r3 = Route(route_name="go play hockey", timestamp=timestamp, user_id=u2.id)
    db.session.add_all([r1, r2, r3])
    db.session.commit()
    return (r1, r2, r3)

def checkpoint_setups_for_tests(u1, u2):
    """setup checkpoins for testing
    return a list of 6 checkpoints
    4 belonging to user1 and 2 to user2"""
    return [
        Checkpoint(user_id=u1.id, checkpoint_display_name="work", checkpoint_lat=35.190564, checkpoint_lng=-106.580526),
        Checkpoint(user_id=u1.id, checkpoint_display_name="outpost", checkpoint_lat=35.11882, checkpoint_lng=-106.71952),
        Checkpoint(user_id=u1.id, checkpoint_display_name="flying star paseo", checkpoint_lat=35.174078, checkpoint_lng=-106.558918), Checkpoint(user_id=u1.id, checkpoint_display_name="7-11", checkpoint_lat=35.172107, checkpoint_lng=-106.496421),
        Checkpoint(user_id=u2.id, checkpoint_display_name="Smith's parking lot", checkpoint_lat=35.132659, checkpoint_lng=-106.49791),
        Checkpoint(user_id=u2.id, checkpoint_display_name="turnaround",checkpoint_lat=35.158915, checkpoint_lng=-106.496983)
    ]
