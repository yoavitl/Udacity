from database_setup import Base, Shelters, Puppy, Adopter, adopter_table
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import asc, desc, update

engine = create_engine('sqlite:///puppies.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

def CheckAdoptedpuppy(puppuid):
    if session.query(adopter_table).filter_by(puppy_id = puppuid).all():
        return False
    else:
        return True

def AdoptaPuppy(adopterid,puppuid):
    if CheckAdoptedpuppy(puppuid):
        adptr = session.query(Adopter).filter_by(aid = adopterid).one()
        ppy = session.query(Puppy).filter_by(pid = puppuid).one()
        adptr.puppies.append(ppy)
        session.execute("update shelters set current_occupancy = current_occupancy - 1 Where id = {0};".format(ppy.shelter_id))
        session.execute("update puppies SET shelter_id= 0 WHERE pid = '%s';" % ppy.pid)

        session.add(adptr)
        session.commit()
        session.close()
    else:
        print "The puppy is already adopted"
