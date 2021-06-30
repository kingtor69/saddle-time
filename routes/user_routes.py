from api import geocode_from_location
from app import app, CURR_USER, CURR_ROUTE, CURR_CHECKPOINT_LIST, GUEST, loginSession, logoutSession
from flask import Flask, session, render_template, redirect
# , jsonify
from models import User
from forms import NewUserForm
# import requests


@app.route('/users/signup', methods=["GET", "POST"])
def signup_new_user():
    """Sign up new users. Enter into database"""
    form = NewUserForm()
    if form.validate_on_submit():
        new_user = User.hashpass(form.data.username, form.data.password)
        new_user.email = form.data.email
        new_user.first_name = form.data.first_name
        new_user.last_name = form.data.last_name
        new_user.profile_pic_image_url = form.data.profile_pic_image_url
        new_user.fav_bike = form.data.fav_bike
        new_user.bike_image_url = form.data.bike_image_url
        new_user.default_bike_type = form.data.default_bike_type
        new_user.weather_units = form.data.weather_units
        new_user.default_geocode = geocode_from_location(form.data.default_location)
        db.session.add(new_user)
        db.session.commit()
        loginSession(new_user)
        return redirect('/')


    return render_template('new-user.html', form=form)


@app.route('/api/users/<user_id>/edit', methods=["PUT", "PATCH"])
def edit_user_profile():
    """Edit user profile, including preferences such as default route type, metric or imperial units, &c. Will also edit other aspects of a user profile such as bio, favorite bike, &c."""

@app.route('/api/users/<user_id>/delete', methods=["DELETE"])
def delete_user():
    """Permanently deletes a user from the database using HTTP API call."""

@app.route('/login')
def login():
    """logs a user in"""

@app.route('/logout')
def logout():
    """logs a user out"""

