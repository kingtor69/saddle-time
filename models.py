from flask_sqlalchemy import flask_sqlalchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)