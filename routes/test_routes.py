from app import app
from flask import Flask, request, render_template

@app.route('/home_test', methods=["POST"])
def test_home_page():
    """Home page test with test input in query string"""
    return render_template('home.html', weather= request.data)
