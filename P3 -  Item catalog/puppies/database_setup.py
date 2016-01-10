from sqlalchemy import Column, ForeignKey, Integer, String, Float, Date, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine

Base = declarative_base()

adopter_table = Table(
    'association', Base.metadata,
    Column('puppy_id', Integer, ForeignKey('puppies.pid')),
    Column('adopter_id', Integer, ForeignKey('adopter.aid'))
)

class Shelters(Base):
    __tablename__ = 'shelters'

    id = Column(Integer, primary_key=True)
    Sname = Column(String, nullable=False)
    address = Column(String, nullable=False)
    city = Column(String(20), nullable=False)
    state = Column(String(20), nullable=False)
    zipcode = Column(Integer)
    website = Column(String, nullable=False)
    maximum_capacity = Column(Integer, default=30)
    current_occupancy = Column(Integer, default=0)


class Puppy(Base):
    __tablename__ = 'puppies'

    pid = Column(Integer, primary_key=True)
    name =Column(String(80), nullable = False)
    DOB = Column(Date)
    gender = Column(String(6), nullable = False)
    weight = Column(Float)
    picture = Column(String)
    description = Column(String)
    Specialneeds = Column(String)
    shelter_id = Column(Integer,ForeignKey('shelters.id'))
    shelters = relationship(Shelters)

    adopters = relationship("Adopter", secondary=adopter_table, backref="puppies")

class Adopter(Base):
    __tablename__= 'adopter'

    aid = Column(Integer, primary_key=True)
    name =Column(String(80), nullable = False)
    familyName = Column(String(80), nullable = False)

engine = create_engine('sqlite:///puppies.db')
Base.metadata.create_all(engine)
