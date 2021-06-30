from api import geocode_from_location
from app import app
from helpers import login_session, logout_session, CURR_USER, CURR_ROUTE, CURR_CHECKPOINT_LIST, GUEST
from flask import Flask, session, g, render_template, redirect, flash
# , jsonify
from models import db, User
from forms import NewUserForm, LoginForm
# import requests

@app.route('/users/signup', methods=["GET", "POST"])
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
        loginSession(new_user)
        return redirect('/')

    return render_template('new-user.html', form=form)


@app.route('/api/users/<user_id>/edit', methods=["PUT", "PATCH"])
def edit_user_profile():
    """Edit user profile, including preferences such as default route type, metric or imperial units, &c. Will also edit other aspects of a user profile such as bio, favorite bike, &c."""

@app.route('/api/users/<user_id>/delete', methods=["DELETE"])
def delete_user():
    """Permanently deletes a user from the database using HTTP API call."""

@app.route('/login', methods=["GET", "POST"])
def login():
    """logs a user in"""
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        if user: 
            login_session(user)
        else:
            flash('those credentials did not match any known user', 'warning')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    """logs a user out"""
    if CURR_USER in session:
        flash (f'{g.user.username} successfully logged out', 'success')
        logout_session()
        
    return redirect('/')


