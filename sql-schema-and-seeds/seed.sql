-- run this after you've run schema.sql

INSERT INTO users
    (username, email, password, fav_bike, default_bike_type, weather_units)
    VALUES
    ('kingtor', 'tor@hearkitty.com', 'unhashedseedpw', '"Lafayette" (Canondale Crit)', 'road', 'metric');

-- not exactly sure how to do ensure I'm getting that ID in subsequent inserts, so I'm going about it fairly manually
-- SELECT id FROM users
--     WHERE username = 'kingtor'

INSERT INTO routes
    (route_name, bike_type, user_id)
    VALUES
    ('Work to Hockey', 'road', 1);

INSERT INTO checkpoints
    (user_id, checkpoint_display_name, checkpoint_lat, checkpoint_lng)
    VALUES
    (1, 'work', 35.190564, -106.580526);

INSERT INTO checkpoints
    (user_id, checkpoint_display_name, checkpoint_lat, checkpoint_lng)
    VALUES
    (1, 'outpost', 35.11882, -106.71952);

INSERT INTO checkpoints
    (user_id, checkpoint_display_name, checkpoint_lat, checkpoint_lng)
    VALUES
    (1, 'flying star paseo', 35.174078, -106.558918);

INSERT INTO checkpoints
    (user_id, checkpoint_display_name, checkpoint_lat, checkpoint_lng)
    VALUES
    (1, '7-11', 35.172107, -106.496421);

INSERT INTO route_checkpoints
    (route_id, checkpoint_id, route_order)
    VALUES
    (2, 5, 1);

INSERT INTO route_checkpoints
    (route_id, checkpoint_id, route_order)
    VALUES
    (2, 6, 4);

INSERT INTO route_checkpoints
    (route_id, checkpoint_id, route_order)
    VALUES
    (2, 7, 2);

INSERT INTO route_checkpoints
    (route_id, checkpoint_id, route_order)
    VALUES
    (2, 8, 3);
