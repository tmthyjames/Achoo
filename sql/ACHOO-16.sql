
\connect postgres

CREATE DATABASE achoo;

CREATE TABLE users (
    id serial PRIMARY KEY,
    dateof date not null default CURRENT_DATE,
    username varchar(75),
    email varchar(120) unique,
    zipcode integer,
    password varchar(300),
    inhaler integer,
    meds integer,
    lng NUMERIC(12, 9),
    lat NUMERIC(12, 9)
)

CREATE TABLE treatment (
    id serial PRIMARY KEY,
    timestamp BIGINT,
    userid INTEGER,
    lng NUMERIC(12, 9),
    lat NUMERIC(12, 9),
    treatment varchar(100),
    accuracy INTEGER
)
