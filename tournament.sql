-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE TABLE players
(
  player_id serial CONSTRAINT player_id_pk PRIMARY KEY,
  name text
);

CREATE TABLE matches
(
  match_id serial CONSTRAINT match_id_pk PRIMARY KEY,
  w_player_id integer REFERENCES players(player_id),
  l_player_id integer REFERENCES players(player_id)
);

CREATE TABLE player_standings
(
  player_id integer REFERENCES players,
  matches_played integer,
  wins integer
);