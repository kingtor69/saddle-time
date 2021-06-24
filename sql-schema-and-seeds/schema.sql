DROP DATABASE IF EXISTS saddle_time_db;
CREATE DATABASE saddle_time_db;
\c saddle_time_db;

CREATE TABLE users
(
  id SERIAL PRIMARY KEY,
  username TEXT NOT NULL UNIQUE,
  email TEXT NOT NULL,
  password TEXT NOT NULL,
  first_name TEXT,
  last_name TEXT,
  bio VARCHAR(256),
  fav_bike VARCHAR(40),
  bike_image_url TEXT,
  default_bike_type VARCHAR(8) DEFAULT 'regular',
  weather_units VARCHAR(8) DEFAULT 'metric'
);

CREATE TABLE routes
(
  id SERIAL PRIMARY KEY,
  route_name VARCHAR(40) DEFAULT 'untitled',
  bike_type VARCHAR(8) DEFAULT 'regular',
  timestamp TIMESTAMP DEFAULT NOW(),
  user_id INTEGER 
);

CREATE TABLE checkpoints
(
  id SERIAL PRIMARY KEY,
  user_id INTEGER,
  checkpoint_display_name TEXT,
  checkpoint_lat FLOAT NOT NULL,
  checkpoint_lng FLOAT NOT NULL
);

CREATE TABLE route_checkpoints
(
  id SERIAL PRIMARY KEY,
  route_id INTEGER,
  checkpoint_id INTEGER,
  route_order INTEGER NOT NULL
);

ALTER TABLE routes
  ADD CONSTRAINT 
  "routes_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

ALTER TABLE checkpoints
  ADD CONSTRAINT 
  "checkpoints_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

ALTER TABLE route_checkpoints
  ADD CONSTRAINT 
  "route_checkpoints_route_id_fkey" FOREIGN KEY (route_id) REFERENCES routes(id) ON DELETE CASCADE;

ALTER TABLE route_checkpoints
  ADD CONSTRAINT 
  "route_checkpoints_checkpoint_id_fkey" FOREIGN KEY (checkpoint_id) REFERENCES checkpoints(id) ON DELETE CASCADE;

