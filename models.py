from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User model.
    There will be a guest user for routes created by people who haven't signed up and/or aren't logged in.
    """

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    username = db.Column(db.String, 
                         nullable=False, 
                         unique=True)
    profile_pic_image_url = db.Column(db.String)
    email = db.Column(db.String,
                      nullable=False)
    password = db.Column(db.String,
                         nullable=False)    
    first_name = db.Column(db.String)                         
    last_name = db.Column(db.String)                         
    fav_bike = db.Column(db.String(40))
    bike_image_url = db.Column(db.String)
    default_bike_type = db.Column(db.String(8),
                                  default="regular")
    weather_units = db.Column(db.String(8), default="metric")

    route = db.relationship("Route", cascade="all, delete")

    def __repr__(self):
        return f'User#{self.id}: {self.username} {self.email} {self.first_name} {self.last_name} Favorite bike: {self.fav_bike} default routes: {self.default_bike_type}'

    @classmethod
    def hashpass(cls, username, password):
        """generate new user with username and hashed password only, other fields still to be populated"""

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
    """Route model for basic routes. 
    Stores geocoded start and end points, bicycle/route type, 
    and the user_id of the user who created or claims the route. 
    Since a guest user can make a route, this user_id might change if a user signs up and/or logs in after defining a route."""

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

    # TODO: we want to keep the route if the checkpoint is deleted
    # BUT we want to delete the checkpoint if the route is deleted
    checkpoint = db.relationship("Checkpoint", cascade="all, delete")

class Checkpoint(db.Model):
    """Checkpoint model for intermediate geocoded points used as either stopping places or to alter route."""

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
    
    # As a route is being built, x can be changed to reorder locations in the route, but when that route is *saved*, it will have a fixed order of checkpoints

class RouteCheckpoint(db.Model):
    """Route-checkpoint model shows in what route and in what order checkpoints are used."""

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