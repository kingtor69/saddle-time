# from models import Route, User, Checkpoint
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired, Optional, Email

class NewRouteForm(FlaskForm):
    """Form for creating a new route."""
    
    route_name = StringField("Name Your Route")
    start_location = StringField("Starting Location")
    end_location = StringField("Destination Location")
