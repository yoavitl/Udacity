#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Team, Base, Player

engine = create_engine('sqlite:///premierleague.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#Populates the DB with players for all the teams.
Player1 = Player(name="Jamie Vardy", position="Forward", team_id="7", image="http://tinyurl.com/pctodeg")
Player2 = Player(name="Riyad Mahrez", position="Midfielder", team_id="7", image="http://tinyurl.com/pctodeg")
Player3 = Player(name="Romelu Lukaku", position="Forward", team_id="6", image="http://tinyurl.com/pctodeg")
Player4 = Player(name="Harry Kane", position="Forward", team_id="17", image="http://tinyurl.com/pctodeg")
Player5 = Player(name="Ross Barkley", position="Midfielder", team_id="6", image="http://tinyurl.com/pctodeg")
Player6 = Player(name="Mesut Ozil", position="Midfielder", team_id="2", image="http://tinyurl.com/pctodeg")
Player7 = Player(name="Odion Ighalo", position="Forward", team_id="18", image="http://tinyurl.com/pctodeg")
Player8 = Player(name="Alexis Sanchez", position="Forward", team_id="2", image="http://tinyurl.com/pctodeg")
Player9 = Player(name="Dimitri Payet", position="Midfielder", team_id="20", image="http://tinyurl.com/pctodeg")
Player10 = Player(name="Georginio Wijnaldum", position="Midfielder", team_id="11", image="http://tinyurl.com/pctodeg")
Player11 = Player(name="Philippe Coutinho", position="Midfielder", team_id="8", image="http://tinyurl.com/pctodeg")
Player12 = Player(name="Sadio Mane", position="Midfielder", team_id="13", image="http://tinyurl.com/pctodeg")
Player13 = Player(name="Juan Mata", position="Midfielder", team_id="10", image="http://tinyurl.com/pctodeg")
Player14 = Player(name="Yannick Bolasie", position="Midfielder", team_id="5", image="http://tinyurl.com/pctodeg")
Player15 = Player(name="Kevin De Bruyne", position="Midfielder", team_id="9", image="http://tinyurl.com/pctodeg")
Player16 = Player(name="Aleksandar Kolarov", position="Defender", team_id="9", image="http://tinyurl.com/pctodeg")
Player17 = Player(name="Troy Deeney", position="Forward", team_id="18", image="http://tinyurl.com/pctodeg")
Player18 = Player(name="Andre Ayew", position="Midfielder", team_id="16", image="http://tinyurl.com/pctodeg")
Player19 = Player(name="Toby Alderweireld", position="Defender", team_id="17", image="http://tinyurl.com/pctodeg")
Player20 = Player(name="Dusan Tadic", position="Midfielder", team_id="13", image="http://tinyurl.com/pctodeg")
Player21 = Player(name="Sergio Aguero", position="Forward", team_id="9", image="http://tinyurl.com/pctodeg")
Player22 = Player(name="Scott Dann", position="Defender", team_id="5", image="http://tinyurl.com/pctodeg")
Player23 = Player(name="Yaya Toure", position="Midfielder", team_id="9", image="http://tinyurl.com/pctodeg")
Player24 = Player(name="Raheem Sterling", position="Forward", team_id="9", image="http://tinyurl.com/pctodeg")
Player25 = Player(name="Arouna Kone", position="Forward", team_id="6", image="http://tinyurl.com/pctodeg")
Player26 = Player(name="Olvier Giroud", position="Forward", team_id="2", image="http://tinyurl.com/pctodeg")
Player27 = Player(name="Daniel DrinkWater", position="Midfielder", team_id="7", image="http://tinyurl.com/pctodeg")
Player28 = Player(name="Yohan Cabaye", position="Midfielder", team_id="5", image="http://tinyurl.com/pctodeg")
Player29 = Player(name="Christian Eriksen", position="Midfielder", team_id="17", image="http://tinyurl.com/pctodeg")
Player30 = Player(name="Fernandinho", position="Midfielder", team_id="9", image="http://tinyurl.com/pctodeg")
Player31 = Player(name="Santiago Cazorla", position="Midfielder", team_id="2", image="http://tinyurl.com/pctodeg")
Player32 = Player(name="Marc Albrighton", position="Midfielder", team_id="7", image="http://tinyurl.com/pctodeg")
Player33 = Player(name="Nacho Monreal", position="Defender", team_id="2", image="http://tinyurl.com/pctodeg")
Player34 = Player(name="James Milner", position="Midfielder", team_id="8", image="http://tinyurl.com/pctodeg")
Player35 = Player(name="Eric Dier", position="Defender", team_id="17", image="http://tinyurl.com/pctodeg")
Player36 = Player(name="Steven Davis", position="Midfielder", team_id="13", image="http://tinyurl.com/pctodeg")
Player37 = Player(name="Gareth Barry", position="Midfielder", team_id="6", image="http://tinyurl.com/pctodeg")
Player38 = Player(name="cheikhou Kouyate", position="Midfielder", team_id="20", image="http://tinyurl.com/pctodeg")
Player39 = Player(name="Eden Hazard", position="Midfielder", team_id="4", image="http://tinyurl.com/pctodeg")
Player40 = Player(name="Aaron Ramsey", position="Midfielder", team_id="2", image="http://tinyurl.com/pctodeg")
Player41 = Player(name="Dele Alli", position="Midfielder", team_id="17", image="http://tinyurl.com/pctodeg")
Player42 = Player(name="Marko Arnautovic", position="Forward", team_id="14", image="http://tinyurl.com/pctodeg")
Player43 = Player(name="Kyle Walker", position="Defender", team_id="17", image="http://tinyurl.com/pctodeg")
Player44 = Player(name="Aaron Cresswell", position="Defender", team_id="20", image="http://tinyurl.com/pctodeg")
Player45 = Player(name="Bacary Sagna", position="Defender", team_id="9", image="http://tinyurl.com/pctodeg")
Player46 = Player(name="Cesc Fabregas", position="Midfielder", team_id="4", image="http://tinyurl.com/pctodeg")
Player47 = Player(name="Martin Skrtel", position="Defender", team_id="8", image="http://tinyurl.com/pctodeg")
Player48 = Player(name="Laurent Koscielny", position="Defender", team_id="2", image="http://tinyurl.com/pctodeg")
Player49 = Player(name="Robbie Brady", position="Midfielder", team_id="12", image="http://tinyurl.com/pctodeg")
Player50 = Player(name="Chris Smalling", position="Defender", team_id="10", image="http://tinyurl.com/pctodeg")
Player51 = Player(name="Graziano Pelle", position="Forward", team_id="13", image="http://tinyurl.com/pctodeg")
Player52 = Player(name="James Morrison", position="Midfielder", team_id="19", image="http://tinyurl.com/pctodeg")
Player53 = Player(name="Manuel Lanzini", position="Midfielder", team_id="20", image="http://tinyurl.com/pctodeg")
Player54 = Player(name="Daley Blind", position="Midfielder", team_id="10", image="http://tinyurl.com/pctodeg")
Player55 = Player(name="Mousa Dembele", position="Midfielder", team_id="17", image="http://tinyurl.com/pctodeg")
Player56 = Player(name="Anthony Martial", position="Forward", team_id="10", image="http://tinyurl.com/pctodeg")
Player57 = Player(name="James McClean", position="Midfielder", team_id="19", image="http://tinyurl.com/pctodeg")
Player58 = Player(name="Erik Lamela", position="Midfielder", team_id="17", image="http://tinyurl.com/pctodeg")
Player59 = Player(name="Glenn Whelan", position="Midfielder", team_id="14", image="http://tinyurl.com/pctodeg")
Player60 = Player(name="James McArthur", position="Midfielder", team_id="5", image="http://tinyurl.com/pctodeg")
Player61 = Player(name="Petr Cech", position="Goalkeeper", team_id="2", image="http://tinyurl.com/pctodeg")
Player62 = Player(name="Ashley Williams", position="Defender", team_id="16", image="http://tinyurl.com/pctodeg")
Player63 = Player(name="Wilfried Zaha", position="Midfielder", team_id="5", image="http://tinyurl.com/pctodeg")
Player64 = Player(name="NGolo Kante", position="Midfielder", team_id="7", image="http://tinyurl.com/pctodeg")
Player65 = Player(name="Kasper Schmeichel", position="Goalkeeper", team_id="7", image="http://tinyurl.com/pctodeg")
Player66 = Player(name="Erik Pieters", position="Defender", team_id="14", image="http://tinyurl.com/pctodeg")
Player67 = Player(name="Wes Morgan", position="Defender", team_id="7", image="http://tinyurl.com/pctodeg")
Player68 = Player(name="Hector Bellerin", position="Defender", team_id="2", image="http://tinyurl.com/pctodeg")
Player69 = Player(name="Wayne Rooney", position="Forward", team_id="10", image="http://tinyurl.com/pctodeg")
Player70 = Player(name="Jesus Navas", position="Midfielder", team_id="9", image="http://tinyurl.com/pctodeg")
Player71 = Player(name="James McCarthy", position="Midfielder", team_id="6", image="http://tinyurl.com/pctodeg")
Player72 = Player(name="Simon Francis", position="Defender", team_id="1", image="http://tinyurl.com/pctodeg")
Player73 = Player(name="Daryl Janmaat", position="Defender", team_id="11", image="http://tinyurl.com/pctodeg")
Player74 = Player(name="Jose Fonte", position="Defender", team_id="13", image="http://tinyurl.com/pctodeg")
Player75 = Player(name="Matt Ritchie", position="Midfielder", team_id="1", image="http://tinyurl.com/pctodeg")
Player76 = Player(name="Moussa Sissoko", position="Midfielder", team_id="11", image="http://tinyurl.com/pctodeg")
Player77 = Player(name="Robert Huth", position="Defender", team_id="7", image="http://tinyurl.com/pctodeg")
Player78 = Player(name="Glen Johnson", position="Defender", team_id="14", image="http://tinyurl.com/pctodeg")
Player79 = Player(name="Jan Vertonghen", position="Defender", team_id="17", image="http://tinyurl.com/pctodeg")
Player80 = Player(name="Diafra Sakho", position="Forward", team_id="20", image="http://tinyurl.com/pctodeg")
Player81 = Player(name="Bafetimbi Gomis", position="Forward", team_id="16", image="http://tinyurl.com/pctodeg")
Player82 = Player(name="Jack Butland", position="Goalkeeper", team_id="14", image="http://tinyurl.com/pctodeg")
Player83 = Player(name="Bastian Schweinsteiger", position="Midfielder", team_id="10", image="http://tinyurl.com/pctodeg")
Player84 = Player(name="Jason Puncheon", position="Midfielder", team_id="5", image="http://tinyurl.com/pctodeg")
Player85 = Player(name="Bakary Sako", position="Midfielder", team_id="5", image="http://tinyurl.com/pctodeg")
Player86 = Player(name="Nathan Redmond", position="Midfielder", team_id="12", image="http://tinyurl.com/pctodeg")
Player87 = Player(name="Tim Howard", position="Goalkeeper", team_id="6", image="http://tinyurl.com/pctodeg")
Player88 = Player(name="Craig Dawson", position="Defender", team_id="19", image="http://tinyurl.com/pctodeg")
Player89 = Player(name="Diego Costa", position="Forward", team_id="4", image="http://tinyurl.com/pctodeg")
Player90 = Player(name="Mark Noble", position="Midfielder", team_id="20", image="http://tinyurl.com/pctodeg")
Player91 = Player(name="Jonny Howson", position="Midfielder", team_id="12", image="http://tinyurl.com/pctodeg")
Player92 = Player(name="Steven Fletcher", position="Forward", team_id="15", image="http://tinyurl.com/pctodeg")
Player93 = Player(name="Jermain Defoe", position="Forward", team_id="15", image="http://tinyurl.com/pctodeg")
Player94 = Player(name="Gerard Deulofeu", position="Forward", team_id="6", image="http://tinyurl.com/pctodeg")
Player95 = Player(name="Bojan", position="Forward", team_id="14", image="http://tinyurl.com/pctodeg")
Player96 = Player(name="Darren Fletcher", position="Midfielder", team_id="19", image="http://tinyurl.com/pctodeg")
Player97 = Player(name="Willian", position="Midfielder", team_id="4", image="http://tinyurl.com/pctodeg")
Player98 = Player(name="Hugo Lloris", position="Goalkeeper", team_id="17", image="http://tinyurl.com/pctodeg")
Player99 = Player(name="Seamus Coleman", position="Defender", team_id="6", image="http://tinyurl.com/pctodeg")
Player100 = Player(name="Virgil van Dijk", position="Defender", team_id="13", image="http://tinyurl.com/pctodeg")
AVplayer1 = Player(name="Charles N'Zogbia", position="Midfielder", team_id="3", image="https://upload.wikimedia.org/wikipedia/commons/d/dc/Charles_N%27Zogbia.png")
AVplayer2 = Player(name="Brad Guzan", position="Goalkeeper", team_id="3", image="https://upload.wikimedia.org/wikipedia/commons/8/80/Brad_Guzan_USMNT_shaking_hands_%28cropped%29.jpg")
AVplayer3 = Player(name="Joleon Lescott", position="Defender", team_id="3", image="https://upload.wikimedia.org/wikipedia/commons/3/3c/Joleon_Lescott_8696_%2815441498930%29.jpg")
AVplayer4 = Player(name="Scott Sinclair", position="Forward", team_id="3", image="https://upload.wikimedia.org/wikipedia/commons/b/b4/Scott_Sinclair_Swansea_City_warm_up_vs_Arsenal_2011_%28cropped%29.jpg")
MCPlayer1 = Player(name ="Joe Hart",
                    description = "With over 100 Premier League clean sheets, Hart holds the record for the most Premier League Golden Glove awards (four) and has amassed over 50 international caps since his debut in 2008 ",
                    image = "https://upload.wikimedia.org/wikipedia/commons/4/41/Joe_Hart_69775.jpg",
                    position = "GoalKeeper",
                    team_id="9")

session.add(MCPlayer1)
session.add(Player1)
session.add(Player2)
session.add(Player3)
session.add(Player4)
session.add(Player5)
session.add(Player6)
session.add(Player7)
session.add(Player8)
session.add(Player9)
session.add(Player10)
session.add(Player11)
session.add(Player12)
session.add(Player13)
session.add(Player14)
session.add(Player15)
session.add(Player16)
session.add(Player17)
session.add(Player18)
session.add(Player19)
session.add(Player20)
session.add(Player21)
session.add(Player22)
session.add(Player23)
session.add(Player24)
session.add(Player25)
session.add(Player26)
session.add(Player27)
session.add(Player28)
session.add(Player29)
session.add(Player30)
session.add(Player31)
session.add(Player32)
session.add(Player33)
session.add(Player34)
session.add(Player35)
session.add(Player36)
session.add(Player37)
session.add(Player38)
session.add(Player39)
session.add(Player40)
session.add(Player41)
session.add(Player42)
session.add(Player43)
session.add(Player44)
session.add(Player45)
session.add(Player46)
session.add(Player47)
session.add(Player48)
session.add(Player49)
session.add(Player50)
session.add(Player51)
session.add(Player52)
session.add(Player53)
session.add(Player54)
session.add(Player55)
session.add(Player56)
session.add(Player57)
session.add(Player58)
session.add(Player59)
session.add(Player60)
session.add(Player61)
session.add(Player62)
session.add(Player63)
session.add(Player64)
session.add(Player65)
session.add(Player66)
session.add(Player67)
session.add(Player68)
session.add(Player69)
session.add(Player70)
session.add(Player71)
session.add(Player72)
session.add(Player73)
session.add(Player74)
session.add(Player75)
session.add(Player76)
session.add(Player77)
session.add(Player78)
session.add(Player79)
session.add(Player80)
session.add(Player81)
session.add(Player82)
session.add(Player83)
session.add(Player84)
session.add(Player85)
session.add(Player86)
session.add(Player87)
session.add(Player88)
session.add(Player89)
session.add(Player90)
session.add(Player91)
session.add(Player92)
session.add(Player93)
session.add(Player94)
session.add(Player95)
session.add(Player96)
session.add(Player97)
session.add(Player98)
session.add(Player99)
session.add(Player100)
session.add(AVplayer1)
session.add(AVplayer2)
session.add(AVplayer3)
session.add(AVplayer4)
session.commit()
session.close()
