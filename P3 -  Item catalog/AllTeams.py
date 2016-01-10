from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Team, Base, Player

engine = create_engine('sqlite:///premierleague.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#All of Premier League Teams
Team1 = Team(name = "AFC Bournemouth", location = "Dean Court", symbol = "https://upload.wikimedia.org/wikipedia/en/e/e5/AFC_Bournemouth_(2013).svg")
session.add(Team1)
session.commit()

Team2 = Team(name = "Arsenal", location = "Emirates Stadium", symbol = "https://upload.wikimedia.org/wikipedia/en/5/53/Arsenal_FC.svg")
session.add(Team2)
session.commit()

Team3 = Team(name = "Aston Villa", location = "Villa Park", symbol = "https://upload.wikimedia.org/wikipedia/en/1/15/Aston_Villa.svg")
session.add(Team3)
session.commit()

Team4 = Team(name = "Chelsea", location = "Stamford Bridge", symbol = "https://upload.wikimedia.org/wikipedia/en/c/cc/Chelsea_FC.svg")
session.add(Team4)
session.commit()

Team5 = Team(name = "Crystal Palace", location = "Selhurst Park", symbol = "https://upload.wikimedia.org/wikipedia/en/0/0c/Crystal_Palace_FC_logo.svg")
session.add(Team5)
session.commit()

Team6 = Team(name = "Everton", location = "Goodison Park", symbol = "https://upload.wikimedia.org/wikipedia/en/7/7c/Everton_FC_logo.svg")
session.add(Team6)
session.commit()

Team7 = Team(name = "Leicester City", location = "King Power Stadium", symbol = "https://upload.wikimedia.org/wikipedia/en/2/2d/Leicester_City_crest.svg")
session.add(Team7)
session.commit()

Team8 = Team(name = "Liverpool", location = "Anfield", symbol = "https://upload.wikimedia.org/wikipedia/en/0/0c/Liverpool_FC.svg")
session.add(Team8)
session.commit()

Team9 = Team(name = "Manchester City", location = "Etihad Stadium", symbol = "https://upload.wikimedia.org/wikipedia/en/c/cf/Manchester_City.svg")
session.add(Team9)
session.commit()

Team10 = Team(name = "Manchester United", location = "Old Trafford", symbol = "https://upload.wikimedia.org/wikipedia/en/7/7a/Manchester_United_FC_crest.svg")
session.add(Team10)
session.commit()

Team11 = Team(name = "Newcastle United", location = "St James' Park", symbol = "https://upload.wikimedia.org/wikipedia/en/5/56/Newcastle_United_Logo.svg")
session.add(Team11)
session.commit()

Team12 = Team(name = "Norwich City", location = "Carrow Road", symbol = "https://upload.wikimedia.org/wikipedia/en/8/8c/Norwich_City.svg")
session.add(Team12)
session.commit()

Team13 = Team(name = "Southampton", location = "St Mary's Stadium", symbol = "https://upload.wikimedia.org/wikipedia/en/c/c9/FC_Southampton.svg")
session.add(Team13)
session.commit()

Team14 = Team(name = "Stoke City", location = "Britannia Stadium", symbol = "https://upload.wikimedia.org/wikipedia/en/2/29/Stoke_City_FC.svg")
session.add(Team14)
session.commit()

Team15 = Team(name = "Sunderland", location = "Stadium of Light", symbol = "https://upload.wikimedia.org/wikipedia/en/7/77/Logo_Sunderland.svg")
session.add(Team15)
session.commit()

Team16 = Team(name = "Swansea City", location = "Liberty Stadium", symbol = "https://upload.wikimedia.org/wikipedia/en/1/16/Swansea_City_AFC_logo.png")
session.add(Team16)
session.commit()

Team17 = Team(name = "Tottenham Hotspur", location = "White Hart Lane", symbol = "https://upload.wikimedia.org/wikipedia/en/b/b4/Tottenham_Hotspur.svg")
session.add(Team17)
session.commit()

Team18 = Team(name = "Watford", location = "Vicarage Road", symbol = "https://upload.wikimedia.org/wikipedia/en/e/e2/Watford.svg")
session.add(Team18)
session.commit()

Team19 = Team(name = "West Bromwich Albion", location = "The Hawthorns", symbol = "https://upload.wikimedia.org/wikipedia/en/8/8b/West_Bromwich_Albion.svg")
session.add(Team19)
session.commit()

Team20 = Team(name = "West Ham United", location = "Boleyn Ground", symbol = "https://upload.wikimedia.org/wikipedia/en/e/e0/West_Ham_United_FC.svg")
session.add(Team20)
session.commit()

session.close()
