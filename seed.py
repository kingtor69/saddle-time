from app import app
from models import db, User, Route, Checkpoint, RouteCheckpoint

db.drop_all()
db.create_all()

# seed users
u1 = User.hashpass('kingtor', 'roadiemutha')
u1.email='tor@hearkitty.com'
u1.fav_bike='"Lafayette" (Canondale Crit)'
u1.default_bike_type="road"
u1.weather_units="metric"
u2 = User.hashpass('cooogan', 'gravelFTW')
u2.email='pete@cogan.com'
u2.default_bike_type="mountain"
u2.weather_units="imperial"
u3 = User.hashpass('bendyboy', 'gravelontheroad')
u3.email='bendy@getbent.com'
u3.fav_bike="GRAVEL!!!"
u3.default_bike_type="regular"
u3.weather_units="metric"
u4 = User.hashpass('TaskMaster', 'doitandlikeit!')
u4.email="task@master.com"
u4.default_bike_type="road"

db.session.add_all([u1, u2, u3, u4])
db.session.commit()

# seed routes
r1 = Route(route_name="work to hockey", bike_type="road", user_id=u1.id)
r2 = Route(route_name="weeknight ride", bike_type="mountain", user_id=u2.id)
r3 = Route(route_name="left my wallet in El Segundo", bike_type="regular", user_id=u3.id)
r4 = Route(route_name="RPV madness", bike_type="road", user_id=u4.id)
r5 = Route(route_name="Griffith Park Ramble", bike_type="road", user_id=u1.id)

db.session.add_all([r1, r2, r3, r4, r5])
db.session.commit()

# seed checkpoints
cp1 = Checkpoint(user_id=u1.id, checkpoint_display_name="work", checkpoint_lat=35.190564, checkpoint_lng=-106.580526)
cp2 = Checkpoint(user_id=u1.id, checkpoint_display_name="outpost", checkpoint_lat=35.11882, checkpoint_lng=-106.71952)
cp3 = Checkpoint(user_id=u1.id, checkpoint_display_name="flying star paseo", checkpoint_lat=35.174078, checkpoint_lng=-106.558918)
cp4 = Checkpoint(user_id=u1.id, checkpoint_display_name="7-11", checkpoint_lat=35.172107, checkpoint_lng=-106.496421)
cp5 = Checkpoint(user_id=u2.id, checkpoint_display_name="Smith's parking lot", checkpoint_lat=35.132659, checkpoint_lng=-106.49791)
cp6 = Checkpoint(user_id=u2.id, checkpoint_display_name="turnaround",checkpoint_lat=35.158915, checkpoint_lng=-106.496983)
cp7 = Checkpoint(user_id=u3.id, checkpoint_display_name="el segundo", checkpoint_lat=33.920861, checkpoint_lng=-118.415947)
cp8 = Checkpoint(user_id=u3.id, checkpoint_display_name="inglewood", checkpoint_lat=33.961767, checkpoint_lng=-118.353336)
cp9 = Checkpoint(user_id=u4.id, checkpoint_display_name="Manhattan Beach", checkpoint_lat=33.885092, checkpoint_lng=-118.40971)
cpa = Checkpoint(user_id=u4.id, checkpoint_display_name="RPV, baby", checkpoint_lat=34.052238, checkpoint_lng=-118.243344)
cpb = Checkpoint(user_id=u1.id, checkpoint_display_name="Oakwoods", checkpoint_lat=34.13679, checkpoint_lng=-118.34195)
cpc = Checkpoint(user_id=u1.id, checkpoint_display_name="Royce Canyon", checkpoint_lat=34.075166, checkpoint_lng=-118.442371)
cpd = Checkpoint(user_id=u1.id, checkpoint_display_name="The Greek", checkpoint_lat=34.02421, checkpoint_lng=-118.21444)

db.session.add_all([cp1, cp2, cp3, cp4, cp5, cp6, cp7, cp8, cp9, cpa, cpb, cpc, cpd])
db.session.commit()

# seed route_checkpoints
rcp1 = RouteCheckpoint(route_id=r1.id, checkpoint_id=cp1.id, route_order=1)
rcp2 = RouteCheckpoint(route_id=r1.id, checkpoint_id=cp2.id, route_order=4)
rcp3 = RouteCheckpoint(route_id=r1.id, checkpoint_id=cp3.id, route_order=2)
rcp4 = RouteCheckpoint(route_id=r1.id, checkpoint_id=cp4.id, route_order=3)
rcp5 = RouteCheckpoint(route_id=r2.id, checkpoint_id=cp5.id, route_order=1)
rcp6 = RouteCheckpoint(route_id=r2.id, checkpoint_id=cp6.id, route_order=2)
rcp7 = RouteCheckpoint(route_id=r2.id, checkpoint_id=cp5.id, route_order=3)
rcp8 = RouteCheckpoint(route_id=r3.id, checkpoint_id=cp7.id, route_order=2)
rcp9 = RouteCheckpoint(route_id=r3.id, checkpoint_id=cp8.id, route_order=1)
rcpa = RouteCheckpoint(route_id=r3.id, checkpoint_id=cp8.id, route_order=3)
rcpb = RouteCheckpoint(route_id=r4.id, checkpoint_id=cp9.id, route_order=1)
rcpc = RouteCheckpoint(route_id=r4.id, checkpoint_id=cpa.id, route_order=2)
rcpd = RouteCheckpoint(route_id=r4.id, checkpoint_id=cp9.id, route_order=3)

db.session.add_all([rcp1, rcp2, rcp3, rcp4, rcp5, rcp6, rcp7, rcp8, rcp9, rcpa, rcpb, rcpc, rcpd])
db.session.commit()