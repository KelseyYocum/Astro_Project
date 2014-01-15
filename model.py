# import docopt
# 


import config
import bcrypt
from datetime import datetime
import string

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, DateTime, Text

from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref
from sqlalchemy.schema import Table

from flask.ext.login import UserMixin



engine = create_engine(config.DB_URI, echo=False) 
session = scoped_session(sessionmaker(bind=engine,
                         autocommit = False,
                         autoflush = False))

Base = declarative_base()
Base.query = session.query_property()

class User(Base, UserMixin):
    __tablename__ = "users" 
    id = Column(Integer, primary_key=True)
    email = Column(String(64), nullable=False)
    password = Column(String(64), nullable=False)
    username = Column(String(64), nullable=False)
    salt = Column(String(64), nullable=False)

    def set_password(self, password):
        self.salt = bcrypt.gensalt()
        password = password.encode("utf-8")
        self.password = bcrypt.hashpw(password, self.salt)

    def authenticate(self, password):
        password = password.encode("utf-8")
        return bcrypt.hashpw(password, self.salt.encode("utf-8")) == self.password

class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True)
    lat = Column(Integer, nullable = False)
    lng = Column(Integer, nullable = False)
    name = Column(String(64), nullable = False)
    site_type = Column(String(64), nullable = False) #ex: observatory, viewing site, star party
    open_times = Column(String (64), nullable = False)
    description = Column(String(64), nullable = True)
    address = Column(String(64), nullable = True)
    phone = Column(String(64), nullable = True)
    email = Column(String(64), nullable = False)
    url = Column(String(64), nullable = True)
    fee = Column(String(64), nullable = True)



################################################################################

def create_tables():
    Base.metadata.create_all(engine)

    u = User(email="test@test.com", username='Jill')
    u.set_password("bubbles")
    session.add(u)


    u2 = User(email="test2@test.com", username='Paul')
    u2.set_password("unicorn")
    session.add(u2)

    u3 = User(email='test3@test.com', username='Sarah')
    u3.set_password('password')
    session.add(u3)

    sunriver = Location(lat=43.8842, 
                        lng=-121.4375, 
                        name="Oregon Observatory",
                        site_type="Observatory",
                        open_times="9:00pm-11:30pm, Tues-Sun, ",
                        description="We are a private, non profit, educational organization. The Oregon Observatory at Sunriver is part of the Sunriver Nature Center & Observatory. We offer evening viewing programs, solar viewing, and many other educational programs. In addition, we sell, service and repair telescope and related products and boast the largest rocketry store in the Northwest.",
                        address="5724 River Road, Sunriver, Oregon 97707",
                        phone="541-598-4406",
                        email="bob@oregonobservatory.com",
                        url="http://www.oregonobservatory.org",
                        fee="Adults $6, Kids $4" )
    session.add(sunriver)

    chabot = Location(lat=37.816, 
                        lng=-122.1806,
                        name="Chabot Space and Science Center",
                        site_type="Science Center and Observatory",
                        open_times="7:30pm-10:30pm, Friday and Saturday",
                        description= "Chabo's giant, historic telescopes offera unique way to experience the awe and wonder of the Universe. Check out celestial viewing day and night. Our observatory deck offers breathtaking views 1,500 fee about the Bay.",
                        address="10000 Skyline Blvd. Oakland, CA 94619",
                        phone="510-336-7300",
                        email="VisitorInfo@ChabotSpace.org",
                        url="http://www.chabotspace.org")

    session.add(chabot)

    mount_tam = Location(lat=37.910583,
                            lng=-122.612700,
                            name="Mount Tam Lectures",
                            site_type="Public Viewing Event",
                            open_times="April-October",
                            description='The San Francisco Amateur Astronomers again joins the Mt Tam Interpretive Society at the annual Summer Astronomy Program hosting public viewing events from April through October. SFAA members bring their telescopes, big and small, to Rock Springs parking lot and share viewing with the public after the astronomy lecture has concluded.',
                            address="Rock Springs Parking Area, Mt Tamalpais State Park, Ridge Ave, Mill Valley, CA",
                            phone="none",
                            email="http://www.sfaa-astronomy.org/contact-us/",
                            url="http://www.sfaa-astronomy.org/star_parties/mount_tam/")
    session.add(mount_tam)
 

    point_lobos = Location(lat=37.7830,
                            lng=-122.5109,
                            name="City Star Parties - Point Lobos/Lands End",
                            site_type="Public Viewing Event",
                            open_times="Refer to club calendar",
                            description="Come out and join the San Francisco Amateur Astronomers for a great viewing range and low light conditions.  Prior to sun-down we hold a telescope clinic where members can bring their scope questions and have the collective wisdom of your fellow members help guide you.",
                            address="N/A",
                            phone="none",
                            email="http://www.sfaa-astronomy.org/contact-us/",
                            url="http://www.sfaa-astronomy.org/star_parties/city/")
    session.add(point_lobos)

    session.commit()
if __name__ == "__main__":
    create_tables()
