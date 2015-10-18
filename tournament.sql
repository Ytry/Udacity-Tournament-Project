-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE TABLE matches
(
  match_id integer CONSTRAINT matches_pk PRIMARY KEY,
  player_id integer
);

CREATE TABLE player_records
(
  id integer CONSTRAINT player_record_id PRIMARY KEY,
  player_id integer,
  match_id integer REFERENCES matches,
  outcome text
);