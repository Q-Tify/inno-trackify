from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class ActivityType(Base):
    __tablename__ = "Activity_Types"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    icon_name = Column(String(200))


class User(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    username = Column(String(100))
    email = Column(String(50))
    password = Column(String(100))


class Activity(Base):
    __tablename__ = "Activity"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    user_id = Column(Integer, ForeignKey("Users.id"))
    type_id = Column(Integer, ForeignKey("Activity_Types.id"))
    duration = Column(String(50))
    start_time = Column(String(50))
    end_time = Column(String(50))
    description = Column(String(2000))

    # Define the relationship between Activity and ActivityType
    type = relationship("ActivityType")
    user = relationship("User")
