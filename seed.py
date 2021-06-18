from app import app
from models import db, User, Route, Checkpoint
from secrets import guest_pass

db.drop_all()
db.create_all()

