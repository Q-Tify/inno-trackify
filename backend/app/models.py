from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base, engine, SessionLocal


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


Base.metadata.create_all(bind=engine)
# Fill the Users table with some initial data

base_path = "https://raw.githubusercontent.com/Wild-Queue/inno-trackify-icons"

activity_types = [
    {
        "id": 1,
        "name": "Sport",
        "icon_name": f"{base_path}/main/Sport.jpg",
    },
    {
        "id": 2,
        "name": "Health",
        "icon_name": f"{base_path}/main/Health.jpg",
    },
    {
        "id": 3,
        "name": "Sleep",
        "icon_name": f"{base_path}/main/Sleep.jpg",
    },
    {
        "id": 4,
        "name": "Study",
        "icon_name": f"{base_path}/main/Study.jpg",
    },
    {
        "id": 5,
        "name": "Rest",
        "icon_name": f"{base_path}/main/Rest.jpg",
    },
    {
        "id": 6,
        "name": "Eat",
        "icon_name": f"{base_path}/main/Eat.jpg",
    },
    {
        "id": 7,
        "name": "Coding",
        "icon_name": f"{base_path}/main/Coding.jpg",
    },
    {
        "id": 8,
        "name": "Other",
        "icon_name": f"{base_path}/main/Other.jpg",
    },
]

db = SessionLocal()
for activity_type in activity_types:
    db.merge(ActivityType(**activity_type))
db.commit()
