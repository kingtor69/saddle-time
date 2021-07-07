# from models import Route, User, Checkpoint
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField
# might need for checkboxes: 
# , BooleanField
from wtforms.validators import InputRequired, Optional, Email, URL, Length

#################################
########## user forms ###########
#################################

class NewUserForm(FlaskForm):
    """Form for creating a new user account."""

    username = StringField("username", validators=[InputRequired(message="You need a username to create an account.")])
    email = StringField("email address", validators=[InputRequired(message="You must enter an email address."), Email(message="That email address format is invalid.")])
    password = PasswordField("password", validators=[InputRequired(message="You must enter a password.")])
    first_name = StringField("first name")
    last_name = StringField("last name")
    profile_pic_image_url = StringField("profile pic link", validators=[URL(message="That doesn't look like a valid URL."), Optional()])
    fav_bike = StringField("your favorite bike", validators=[Length(max=40, message="Wow, your bike has a long name. Please abbreviate that to 40 characters or fewer."), Optional()])
    bike_image_url = StringField("bike picture link", validators=[URL(message="That doesn't look like a valid URL."), Optional()])
    default_bike_type = SelectField("default bike route type", choices=[('regular', "it's just a bike, man"), ('road', "roadie"), ('electric', 'electric'), ('mountain', 'mountain')])
    default_location = StringField('your default route starting point')
    weather_units = SelectField("default weather units", choices=[('metric', '℃/kmph'), ('imperial', '℉/mph')])

class LoginForm(FlaskForm):
    """Form to log in existing user."""

    username = StringField("username", validators=[InputRequired(message="You must enter a username to log in.")])
    password = PasswordField("password", validators=[InputRequired(message="You must enter a password to log in.")])


#################################
######### route forms ###########
#################################

class NewRouteForm(FlaskForm):
    """Form for creating a new route."""
    
    route_name = StringField("Name Your Route")
    bike_type = SelectField("Route Type (type of bike)", choices=[('regular', "It's Just a Bike"), ('road', 'Road Bike'), ('mountain', 'Mountain Bike'), ('electric', 'Electric Bike')])

class NewCheckpointForm(FlaskForm):
    """Form for creating a new checkpoint."""
    checkpoint_name = StringField("Checkpoint Name")
    cp_location = SelectField("Checkpoint Location", choices=[('', 'location')])
    # that choice is a placeholder, actually choices will be changed in javascript with autocomplete data from mapbox API



################ not currently using this form, but not ready to delete it just yet
# class WeatherPrefsForm(FlaskForm):
#     """Simple form for user's location and favorite weather units."""
# 
#     location = StringField("Location")
#     units = SelectField("Units", choices=[('metric', '℃/kmph'), ('imperial', '℉/mph')])