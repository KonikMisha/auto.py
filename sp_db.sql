CREATE TABLE IF NOT EXISTS users (
id integer PRIMARY KEY AUTHORIZATION,
name text NOT NULL,
email text NOT NULL,
psw text NOT NULL,
time integer NOT NULL
);