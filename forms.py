# from models import Route, User, Checkpoint
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField
from wtforms.validators import InputRequired, Optional, Email, URL, Length

#################################
########## user forms ###########
#################################
class UserNewForm(FlaskForm):
    """Form for creating a new user account."""

    username = StringField("username", validators=[InputRequired(message="You need a username to create an account.")])
    email = StringField("email address", validators=[InputRequired(message="You must enter an email address."), Email(message="That email address format is invalid.")])
    password = PasswordField("password", validators=[InputRequired(message="You must enter a password.")])
    first_name = StringField("first name")
    last_name = StringField("last name")
    profile_pic_image_url = StringField("profile pic link", validators=[Optional()])
    fav_bike = StringField("your favorite bike", validators=[Length(max=40, message="Wow, your bike has a long name. Please abbreviate that to 40 characters or fewer."), Optional()])
    bike_image_url = StringField("bike picture link", validators=[Optional()])
    units = SelectField("default weather units", choices=[('metric', '℃/kmph'), ('imperial', '℉/mph')])

class UserEditForm(FlaskForm):
    """Form for editing a user's profile."""
    email = StringField("email address", validators=[InputRequired(message="You must enter an email address."), Email(message="That email address format is invalid.")])
    first_name = StringField("first name")
    last_name = StringField("last name")
    profile_pic_image_url = StringField("profile pic link")
    fav_bike = StringField("your favorite bike", validators=[Length(max=40, message="Wow, your bike has a long name. Please abbreviate that to 40 characters or fewer."), Optional()])
    bike_image_url = StringField("bike picture link")
    units = SelectField("default weather units", choices=[('metric', '℃/kmph'), ('imperial', '℉/mph')])

class LoginForm(FlaskForm):
    """Form to log in existing user."""

    username = StringField("username", validators=[InputRequired(message="You must enter a username to log in.")])
    password = PasswordField("password", validators=[InputRequired(message="You must enter a password to log in.")])


#################################
######### route forms ###########
#################################
class NewCheckpointForm(FlaskForm):
    """Form for creating a new checkpoint."""
    cp_name = StringField(render_kw={"placeholder": "checkpoint name (optional)"})
    cp_location = SelectField(validators=[InputRequired(message="you must have a location")])

class LocationForm(FlaskForm):
    location = SelectField("Location", validators=[InputRequired(message="you must have a location")])