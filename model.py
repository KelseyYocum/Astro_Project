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
    description = Column(String(64), nullable = True)


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

    santa_fe = Location(lat = 35.6672, lng = -105.9644, description = "this is a test")
    albuquerque = Location(lat = 35.1107, lng = -106.6100, description = "this is another test")
    taos = Location(lat = 36.3940, lng = -105.5767, description = "this is a test again")
    session.add(santa_fe)
    session.add(albuquerque)
    session.add(taos)

  
    session.commit()

if __name__ == "__main__":
    create_tables()
