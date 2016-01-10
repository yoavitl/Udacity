from database_setup import Base, Shelters, Puppy, Adopter
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import asc, desc, update
import random
import datetime


engine = create_engine('sqlite:///puppies.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

Puppies = session.execute('select * from puppies order by name;').fetchall()
selter = session.execute('select * from shelters;').fetchall()

countselter = session.execute('select count(*),shelter_id from puppies group by shelter_id;').fetchall()

def addPuppy():
    def CreateRandomAge():
    	today = datetime.date.today()
    	days_old = random.randint(0,540)
    	birthday = today - datetime.timedelta(days = days_old)
    	return birthday

    def addPuppytoDB(*arg):
        shelterin = random.randint(1,5)
        Checkpuppiespopulation(shelterin)
        addpuppy = Puppy(name = '%s' % name, DOB = CreateRandomAge(), gender = '%s' % gender, weight = random.uniform(1.0, 40.0),
         picture = '%s' % picture, description ='%s' % description, Specialneeds = '%s' % Specialneeds, shelter_id = '%s' % shelterin)
        session.add(addpuppy)
        session.commit()
    name = raw_input("what's the puppy name?")
    gender = raw_input("what's the puppy gender?")
    picture = raw_input("picture ?")
    description = raw_input("descript the Puppy?")
    Specialneeds = raw_input("what's the puppy speacial needs?")
    addPuppytoDB(name,gender,picture,description,Specialneeds)


def Checkpuppiespopulation(shelterid):
    shelter_state = session.query(Shelters).filter_by(id = shelterid).one()
    if shelter_state.current_occupancy < shelter_state.maximum_capacity:
        return True
    else:
      print "The shelter is fully booked, Try different shelter:"
      Finddifferentshelter()


def Finddifferentshelter():
    vacant_shelters= session.query(Shelters).all()
    for i in vacant_shelters:
        if i.current_occupancy <= i.maximum_capacity:
            print i.Sname + "\tid:{}".format(i.id)
        


def LoadBalance():
    def movepuppieshelter(froms,tos):
        move_puppie = session.query(Puppy).filter_by(shelter_id = froms).limit(1).offset(0).one()
        session.execute("update puppies SET shelter_id='%s' WHERE pid = '%s';" % (tos, move_puppie.pid))
        session.execute("update shelters set current_occupancy = current_occupancy - 1 Where id = {0};".format(froms))
        session.execute("update shelters set current_occupancy = current_occupancy + 1 Where id = {0};".format(tos))
        session.commit()
        print "the Puppy {0} have moved to this {1} Shelter!".format(move_puppie.name, tos)



    avg_shelter = session.execute('select round(avg(current_occupancy),0) from shelters;').fetchone()
    shelter_diff= session.query(Shelters).all()
    for i in shelter_diff:
        diff = int(i.current_occupancy - avg_shelter[0])
        print "{0} is {1} puppies from the avargae\n".format(i.Sname, diff)
        if diff > 0:
            print "so lets move %i from this shleter\n" % diff
            for sltr in range(diff):
                sheltertomove = range(1,6)
                sheltertomove.pop(i.id-1)
                toshelter = random.choice(sheltertomove)
                movepuppieshelter(i.id,toshelter)

def SetPuppiesOccupancy():
    for s in selter:
        for i in countselter:
            if i[1] == s.id:
                session.execute("update shelters SET current_occupancy='%s' WHERE id = '%s';" % (i[0], s.id))
                session.commit()


session.close()
