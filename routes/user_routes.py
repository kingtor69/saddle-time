# from app import app
from helpers import login_session, logout_session, CURR_USER, CURR_ROUTE, CURR_CHECKPOINT_LIST, GUEST, geocode_from_location
from flask import Flask, session, g, Blueprint, render_template, redirect, flash
# , jsonify
from models import db, User
from forms import NewUserForm, LoginForm
# import requests

from flask import Blueprint, render_template

user_routes = Blueprint("user_routes", __name__, static_folder="../static", template_folder="../templates")

@user_routes.route('/users/signup', methods=["GET", "POST"])
def signup_new_user():
    """Sign up new users. Enter into database"""

    form = NewUserForm()
    if form.validate_on_submit():
        new_user = User.hashpass(form.username.data, form.password.data)
        new_user.email = form.email.data
        new_user.first_name = form.first_name.data
        new_user.last_name = form.last_name.data
        new_user.profile_pic_image_url = form.profile_pic_image_url.data
        new_user.fav_bike = form.fav_bike.data
        new_user.bike_image_url = form.bike_image_url.data
        new_user.default_bike_type = form.default_bike_type.data
        new_user.weather_units = form.weather_units.data
        new_user.default_geocode = geocode_from_location(form.default_location.data)
        db.session.add(new_user)
        db.session.commit()
        login_session(new_user)
        return redirect('/')

    return render_template('new-user.html', form=form)


@user_routes.route('/users/<int:user_id>')
def show_user_profile(user_id):
    """Show user profile to anyone. Show user's default current weather location and most recent route to a logged in user viewing their own page. This is the user's landing page after logging in."""
    user = User.query.get_or_404(user_id)
    user.full_name = user.make_full_name()
    return render_template ('user.html', user=user)


@user_routes.route('/api/users/<user_id>/edit', methods=["PUT", "PATCH"])
def edit_user_profile():
    """Edit user profile, including preferences such as default route type, metric or imperial units, &c. Will also edit other aspects of a user profile such as bio, favorite bike, &c."""

@user_routes.route('/api/users/<user_id>/delete', methods=["DELETE"])
def delete_user():
    """Permanently deletes a user from the database using HTTP API call."""

@user_routes.route('/login', methods=["GET", "POST"])
def login():
    """logs a user in"""
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        if user: 
            login_session(user)
            return redirect(f'/users/{user.id}')
        else:
            flash('those credentials did not match any known user', 'warning')
            return redirect ('/login')

    return render_template('login.html', form=form)

@user_routes.route('/logout')
def logout():
    """logs a user out"""
    if CURR_USER in session:
        logging_out_user = g.user.username
        flash (f'{logging_out_user} successfully logged out', 'success')
        logout_session()
        
    return redirect('/')


#######################################
##### routes for development only #####
#####    delete on deployment     #####
#######################################

@user_routes.route('/home_test', methods=["GET", "POST"])
def test_home_page():
    """Home page test with test in POST route."""
    import pdb
    pdb.set_trace()
    weather={}
    weather['city'] = request.city.data
    weather['conditions'] = request.conditions.data
    weather['weather_icon_url'] = request.weather_icon_url.data
    weather['current_weather_details'] = {}
    current_weather_details_obj = request.current_weather_details.data


    weather['current_weather_details']['Temperature'] = current_weather_details_obj['Temperature']
    weather['current_weather_details']['High'] = current_weather_details_obj['High']
    weather['current_weather_details']['Low'] = current_weather_details_obj['Low']
    weather['current_weather_details']['Feels Like'] = current_weather_details_obj['Feels Like']
    weather['current_weather_details']['Relative Humidity'] = current_weather_details_obj['Relative Humidity']
    weather['current_weather_details']['Wind Speed'] = current_weather_details_obj['Wind Speed']
    weather['current_weather_details']['Wind Direction'] = current_weather_details_obj['Wind Direction']

    return render_template('home.html', weather=weather)

@user_routes.route('/pdb', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def pdb_set_trace():
    """defined this route for debugging purposes"""
    import pdb
    pdb.set_trace()
    return redirect('/')

