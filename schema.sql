DROP DATABASE IF EXISTS saddle_time_db;
CREATE DATABASE saddle_time_db;
/c saddle_time_db;

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
  default_bike_type VARCHAR(8) DEFAULT "regular",
  weather_units VARCHAR(8) DEFAULT "metric"
);

CREATE TABLE routes
(
  id SERIAL PRIMARY KEY,
  route_name VARCHAR(40) DEFAULT "untitled",
  -- start_display_name VARCHAR(40),
  -- start_lat FLOAT NOT NULL,
  -- start_lng FLOAT NOT NULL,
  -- end_display_name VARCHAR(40),
  -- end_lat FLOAT NOT NULL,
  -- end_lng FLOAT NOT NULL,
  bike_type VARCHAR(8) DEFAULT "regular",
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  user_id INTEGER FOREIGN KEY REFERENCES users ON DELETE CASCADE
);

CREATE TABLE checkpoints
(
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL FOREIGN KEY REFERENCES users ON DELETE CASCADE,
  checkpoint_display_name TEXT,
  checkpoint_lat FLOAT NOT NULL,
  checkpoint_lng FLOAT NOT NULL
);

CREATE TABLE route_checkpoints
(
  id SERIAL PRIMARY KEY,
  route_id INTEGER NOT NULL FOREIGN KEY REFERENCES routes ON DELETE CASCADE,
  checkpoint_id INTEGER NOT NULL FOREIGN KEY REFERENCES checkpoints ON DELETE CASCADE,
  route_order INTEGER NOT NULL
)