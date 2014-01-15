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
    address = Column(String(64), nullable = False)
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
                        open_times="Summer Tues-Sun",
                        description="We are a private, non profit, educational organization. The Oregon Observatory at Sunriver is part of the Sunriver Nature Center & Observatory. We offer evening viewing programs, solar viewing, and many other educational programs. In addition, we sell, service and repair telescope and related products and boast the largest rocketry store in the Northwest.",
                        address="5724 River Road, Sunriver, Oregon 97707",
                        phone="541-598-4406",
                        email="bob@oregonobservatory.com",
                        url="www.oregonobservatory.org",
                        fee="Adults $6, Kids $4" )
    session.add(sunriver)
  
    session.commit()

if __name__ == "__main__":
    create_tables()
