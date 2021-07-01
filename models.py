from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User model. user.id is used in Route and Checkpoint models as those will both be stored within the user. 
    """

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    username = db.Column(db.String, 
                         nullable=False, 
                         unique=True)
    email = db.Column(db.String,
                      nullable=False)
    password = db.Column(db.String,
                         nullable=False)
    first_name = db.Column(db.String)                         
    last_name = db.Column(db.String)                         
    profile_pic_image_url = db.Column(db.String)
    fav_bike = db.Column(db.String(40))
    bike_image_url = db.Column(db.String, default="/static/images/saddletime-default-bike.png")
    default_bike_type = db.Column(db.String(8),
                                  default="regular")
    default_geocode_lat = db.Column(db.Float)
    default_geocode_lng = db.Column(db.Float)
    weather_units = db.Column(db.String(8), default="metric")

    route = db.relationship("Route", backref="user_route", cascade="all, delete")
    checkpoint = db.relationship("Checkpoint", backref="user_checkpoint", cascade="all, delete")

    def __repr__(self):
        return f'User#{self.id}: {self.username} {self.email} {self.first_name} {self.last_name} Favorite bike: {self.fav_bike} default routes: {self.default_bike_type}'

    def make_full_name(self):
        """return a full name for users' first_name + last_name"""
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        else:
            return self.first_name or self.last_name or None

    @classmethod
    def hashpass(cls, username, password):
        """Generate new user with username and hashed password only, other fields still to be populated.
        """

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")

        return cls(username=username, password=hashed_utf8)

    @classmethod
    def authenticate(cls, username, password):
        """Validate correct username and password combination.
        Return user if valid, False if not.
        """

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user

        return False

class Route(db.Model):
    """Route model for basic routes. Routes are linked to user_id of the user who created or claims the route. If another user sees a route they like and wants to make it their own, it will be copied to a new entry so that user can change or adapt the route without changing anything for the original user. Timestamp is updated whenever a new API call is made for the route, which will be done when anyone is viewing a route with a timestamp more than a fortnight in the past.
    """

    __tablename__ = "routes"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    route_name = db.Column(db.String(40),
                           default="untitled")  
    bike_type = db.Column(db.String(8),
                          default="regular")
    timestamp = db.Column(db.DateTime,
                          default=datetime.utcnow())
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.id"))

    checkpoint_route = db.relationship("RouteCheckpoint", backref="route_checkpoint", cascade="all, delete")

class Checkpoint(db.Model):
    """Checkpoint model for intermediate geocoded points used as either stopping places or to alter route. Checkpoints are saved with user who created them and associated with routes in the ORM RouteCheckpoint (below). They can be copied by other users who see a checkpoint they want to use in their own route. 
    """

    __tablename__ = "checkpoints"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.id"))
    checkpoint_display_name = db.Column(db.String)
    checkpoint_lat = db.Column(db.Float,
                        nullable=False)
    checkpoint_lng = db.Column(db.Float,
                        nullable=False)
    
class RouteCheckpoint(db.Model):
    """Route-checkpoint model shows in what route and in what order checkpoints are used. These are not linked directly to user who created them because both the route and the checkpoint are. 
    """

    __tablename__ = "route_checkpoints"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    route_id = db.Column(db.Integer,
                         db.ForeignKey("routes.id"))
    checkpoint_id = db.Column(db.Integer,
                              db.ForeignKey("checkpoints.id"))
    route_order = db.Column(db.Integer,
                            nullable=False)