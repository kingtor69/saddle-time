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
  start TEXT NOT NULL,
  end TEXT NOT NULL,
  bike_type TEXT DEFAULT "regular"
  user_id INTEGER REFERENCES users ON DELETE CASCADE
);

CREATE TABLE checkpoints
(
  id SERIAL PRIMARY KEY,
  route_id INTEGER NOT NULL REFERNCES routes ON DELETE CASCADE,
  pt-x TEXT NOT NULL,
  x INTEGER NOT NULL
);