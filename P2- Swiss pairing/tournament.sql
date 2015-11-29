-- Table definitions for the tournament project.

-- The Primary table which connects the players and their id
CREATE TABLE Players (Id SERIAL Primary Key not null, 
					 Full_Name TEXT not null);

-- The second table that registers and save the match data for the players
CREATE TABLE Player_Record (Id int not null,
							Foreign Key(Id) REFERENCES Players(Id) ON DELETE CASCADE,
							Record Integer not null,
							Matches_played integer not null);

-- This table saves the data about each match- the players and who won. the match id is unique
CREATE TABLE Match_Record (Match_Id SERIAL Primary Key not null,
							Player1 int not null, 
							Foreign key (Player1) REFERENCES Players(Id) ON DELETE CASCADE,
							Player2  int, 
							Foreign key (Player2) REFERENCES Players(Id) ON DELETE CASCADE,
							Winner int, 
							Foreign key (Winner) REFERENCES Players(Id) ON DELETE CASCADE); 

-- This view organizes the players by their rank.
CREATE VIEW Players_Rank AS Select players.id,players.Full_Name,Player_Record.Record,Player_Record.Matches_played from Player_Record
							join Players on Player_Record.id = Players.id order by Record desc;

