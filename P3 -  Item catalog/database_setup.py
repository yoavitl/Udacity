import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


# Creates a table to write the users that log in to the application
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    email = Column(String)


# Creates a table for all the premier league teams
class Team(Base):
    __tablename__ = 'team'

    id = Column(Integer, primary_key=True)
    name = Column(String(60), nullable=False)
    location = Column(String(50))
    symbol = Column(String)

    # Helps creates a JSON for all the premier league teams
    @property
    def serialize(self):

        return {
            'id': self.id,
            'name': self.name,
            'symbol': self.symbol,
            'location': self.location,
        }


# Creates a table for players in the teams
class Player(Base):
    __tablename__ = 'players'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    image = Column(String)
    position = Column(String(50))
    team_id = Column(Integer, ForeignKey('team.id'))
    team = relationship(Team)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(User)

    # Helps tp create a JSON for the players
    @property
    def serialize(self):

        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'image': self.image,
            'position': self.position,
        }


engine = create_engine('sqlite:///premierleague.db')
Base.metadata.create_all(engine)
