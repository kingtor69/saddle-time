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
  bio TEXT,
  fav_bike TEXT,
  default_bike_type TEXT DEFAULT "regular"
);

CREATE TABLE routes
(
  id SERIAL PRIMARY KEY,
  route_name TEXT DEFAULT "untitled",
  start_display_name TEXT,
  start_lat FLOAT NOT NULL,
  start_lng FLOAT NOT NULL,
  end_display_name TEXT,
  end_lat FLOAT NOT NULL,
  end_lng FLOAT NOT NULL,
  bike_type TEXT DEFAULT "regular",
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  user_id INTEGER FOREIGN KEY REFERENCES users ON DELETE CASCADE
);

CREATE TABLE checkpoints
(
  id SERIAL PRIMARY KEY,
  route_id INTEGER NOT NULL FOREIGN KEY REFERENCES routes ON DELETE CASCADE,
  pt_x_display_name TEXT,
  pt_x_lat FLOAT NOT NULL,
  pt_x_lng FLOAT NOT NULL,
  x INTEGER NOT NULL
);

