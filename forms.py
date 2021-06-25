# from models import Route, User, Checkpoint
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import InputRequired, Optional, Email

class NewRouteForm(FlaskForm):
    """Form for creating a new route."""
    
    route_name = StringField("Name Your Route")
    start_location = StringField("Starting Location")
    end_location = StringField("Destination Location")

################ not currently using this form, but not ready to delete it just yet
# class WeatherPrefsForm(FlaskForm):
#     """Simple form for user's location and favorite weather units."""
# 
#     location = StringField("Location")
#     units = SelectField("Units", choices=[('metric', '℃/kmph'), ('imperial', '℉/mph')])