#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament

import psycopg2
import random


def ConnectAndCommit(query, *args):
    """Connect to the PostgreSQL database.  Manipulate Data in the database."""
    DB = psycopg2.connect("dbname=tournament")
    cur = DB.cursor()
    cur.execute(query, *args)
    DB.commit()
    DB.close()


def ConnectAndAsk(query):
    """Connect to the PostgreSQL database.  Returns a database query."""
    global resualts
    DB = psycopg2.connect("dbname=tournament")
    cur = DB.cursor()
    cur.execute(query)
    resualts = cur.fetchall()
    DB.close()


def deleteMatches():
    """Resets the matches table. for a clear tournament"""
    ConnectAndCommit("Drop Table Match_Record;")
    ConnectAndCommit("""
        CREATE TABLE Match_Record (Match_Id SERIAL Primary Key,
                            Player1 int REFERENCES Players(Id),
                            Player2  int REFERENCES Players(Id),
                            Winner int REFERENCES Players(Id)); """)


def CheckIfPlayerIsExist(Player_name):
    """ Checks in the database if the player name is exist, ot if there is more then one player with that name"""  # noqa
    ConnectAndAsk("Select count(*) from players where Full_name = ('%s');" % Player_name.lower())  # noqa
    global player_exist
    for row in resualts:
        if int(row[0]) == 1:
            player_exist = 1
        elif int(row[0]) > 1:
            player_exist = 2
        else:
            player_exist = 0


def deletePlayers(Player_name):
    """Remove all the player records from the database."""
    CheckIfPlayerIsExist(Player_name)
    if Player_name == 'all':
        ConnectAndCommit("Delete From players")
    elif player_exist == 1:
        ConnectAndCommit("Delete From players where Full_name = ('%s');" % Player_name)  # noqa
        print "The player was deleted"
    elif player_exist == 2:
        print "There is more then one player with this name."
    else:
        print "There was a error with your player name"


def countPlayers():
    """Returns the number of players currently registered."""
    ConnectAndAsk("Select count(*) from players;")
    return int(resualts[0][0])


def Numberpfplyerscheck():
    """ check if there is an odd or equal number of players"""
    if countPlayers() % 2 == 0:
        print "There is an equal number of players"
    else:
        print "There is uneven number of players"


def registerPlayer(Player_name):
    """Adds a player to the tournament database.
    Args:
      name: the player's full name (need not be unique).
    """
    ConnectAndCommit("insert into players values (default,%s); Insert into player_record values (currval('players_id_seq'),0,0);", (Player_name,))  # noqa


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    ConnectAndAsk("Select * from players_rank;")
    place = 1
    # these lines of code print in the console the current standings
    # in a tabular way) this paert could be commented out.
    for row in resualts:
        print "%s Place:" % place
        print('id: %s \t Name: %s \t Wins: %s \tMatches: %s\n' % row)
        place += 1
    print "---------------------------------------------------------"
    return resualts


def reportMatch(Player1, Player2):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    winner = random.choice([Player1, Player2])
    ConnectAndCommit("""Insert into Match_Record values(default, %s, %s, %s);
                        Update player_record set matches_played = matches_played +1 where id in(%s,%s);
                        Update player_record set record = record +1 where id = %s;""" % (Player1, Player2, winner, Player2, Player1, winner))   # noqa


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
    pairs = []
    for i in range(0, countPlayers(), 2):
        ConnectAndAsk("Select id,full_name from players_rank limit 2 offset %i;" % i)  # noqa
        res = (resualts[0][0],  resualts[0][1], resualts[1][0], resualts[1][1])
        pairs += [res]
    return pairs
