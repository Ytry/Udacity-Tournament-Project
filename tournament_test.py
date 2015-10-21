#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    cur = db.cursor()
    cur.execute("DELETE FROM matches")
    db.commit()
    db.close


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    cur = db.cursor()
    cur.execute("DELETE FROM player_standings")
    db.commit()
    cur.execute("DELETE FROM players")
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    cur = db.cursor()
    cur.execute("SELECT count(player_id) FROM players")
    count = cur.fetchall()
    db.close()
    return count[0][0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """

    db = connect()
    cur = db.cursor()
    cur.execute("INSERT INTO players(name) VALUES (%s)", (name,))
    db.commit()
    cur.execute("INSERT INTO player_standings (player_id, matches_played, wins) VALUES ((SELECT player_id FROM players where name = %s ),0,0)", (name,))  # noqa
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player # noqa
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    cur = db.cursor()
    cur.execute("SELECT players.player_id, name, wins, matches_played FROM players, player_standings WHERE players.player_id = player_standings.player_id ORDER BY wins desc")  # noqa
    standings = cur.fetchall()
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    cur = db.cursor()
    cur.execute("INSERT INTO matches (w_player_id, l_player_id) VALUES (%s, %s)", (winner, loser,))  # noqa
    db.commit()
    cur.execute("UPDATE player_standings SET matches_played = matches_played+1, wins = wins+1 WHERE player_standings.player_id = %s ", (winner,))  # noqa
    db.commit()
    cur.execute("UPDATE player_standings SET matches_played = matches_played+1 WHERE player_standings.player_id = %s ", (loser,))  # noqa
    db.commit()
    db.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
