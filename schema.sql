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
  favorite_bike TEXT
);

CREATE TABLE routes
(
  id SERIAL PRIMARY KEY,
  route_name TEXT DEFAULT "untitled",
  start TEXT NOT NULL,
  end TEXT NOT NULL
)