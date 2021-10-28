from app import app
from models import db, User, Route, Checkpoint, CheckpointRoute

db.drop_all()
db.create_all()

# seed user
u1 = User.hashpass('kingtor', 'road13mutH4!')
u1.email='tor@hearkitty.com'
u1.fav_bike="The one I don't have yet...."
u1.default_bike_type="road"
u1.units="metric"
u1.default_geocode_lat=35.190564
u1.default_geocode_lng=-106.580526
u1.bike_image_url="/static/images/94422-50_ROUBAIX-COMP-REDTNT-METWHTSIL_HERO.webp"
u1.profile_pic_image_url="/static/images/torRoadieProfilePic.jpg"

db.session.add(u1)
db.session.commit()