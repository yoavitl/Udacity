Swiss Pairing Project v1.0
---------------------------

This python and sql code helps create a database for a competition
that is held by the swiss pairing system (e.g: Chess Tournament.)
The folder also contains a file that helps checking the software.

The repository contains.
------------------------

1 - tournament.sql
	This is a .sql scripts that will create the necessary database to manage
	the registration of players and matches.

2 - tournament.py
	This is a python module that contains the necessary functions for running
	the tournament. It also Contains function for deleting the registry 
	for players and matches.

3 - tournament_test.py
	This python file is used to run test cases on the python module 
	tournament.py, and to check that everything is happing according to plan

How to run the application.
---------------------------

You need to have python 2.7 installed on the computer.
You Need a computer with postgres sql installed 
and psycopg2 python module installed. 

1 - open the terminal and enter the command "psql" 
2 - after you have connected to the postgres enter these commands-
	$ create database tournament;
	$ \c tournament;
	$ \i tournament.sql;
3 - you have now created the database and the needed tables. 
	in the terminal run this command - 
	$ python tournament_test.py 

This will run all the test cases to check the module. if all is working
you should get the message - "Success!  All tests pass!".
Then you will see table of a mock up tournament and their standing through
the different phases of the tournament, and you should see who won the tournament.

Copyright:  Yoavi
Auther:     Yoav T. Levi
Date:       11.11.15
