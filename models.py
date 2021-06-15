from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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
    fav_bike = db.Column(db.String)
    bike_image_url = db.Column(db.String)
    default_bike_type = db.Column(db.String,
                                  default="regular")

    def __repr__(self):
        return f'User#{self.id}: {self.username} {self.email} {self.first_name} {self.last_name} Favorite bike: {self.fav_bike} default routes: {self.default_bike_type}'

class Route(db.Model):
    """Route model for basic routes. 
    Stores geocoded start and end points, bicycle/route type, 
    and the user_id of the user who created or claims the route. 
    Since a guest user can make a route, this user_id might change if a user signs up and/or logs in after defining a route."""

    __tablename__ = "routes"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    route_name = db.Column(db.String,
                           default="untitled")                   
    start = db.Column(db.String,
                      nullable=False)                           
    end = db.Column(db.String,
                    nullable=False)                      
    bike_type = db.Column(db.String,
                          default="regular")
    user_id = db.Column(db.Integer
                        db.ForeignKey('users.id'))

class Checkpoint(db.Model):
    """Checkpoint model for intermediate geocoded points used as either stopping places or to alter route."""

    __tablename__ = "checkpoints"

    route_id = db.Column(db.Integer,
                         db.ForeignKey('routes.id')
                         primary_key=True)
    x = db.Column(db.Integer,
                  primary_key=True)
    point_x = db.Column(db.String,
                        nullable=False)