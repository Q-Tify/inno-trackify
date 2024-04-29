from sqlalchemy.orm import Session
from .. import models
from ..schemas import activities as schemas


# Функция для получения всех активностей
def get_activities(db: Session, user_id: int):
    return (
        db.query(models.Activity)
        .filter(models.Activity.user_id == user_id)
        .all()
    )


# Функция для получения всех активностей по типу
def get_activities_by_type(db: Session, user_id: int, type: str):
    type = (
        db.query(models.ActivityType)
        .filter(models.ActivityType.name == type)
        .first()
    )
    return (
        db.query(models.Activity)
        .filter(
            models.Activity.type_id == type.id and models.Activity.user_id == user_id
        )
        .all()
    )


# Функция для получения всех активностей по дате
def get_activities_by_date(db: Session, user_id: int, date: str):
    return (
        db.query(models.Activity)
        .filter(
            models.Activity.start_time.contains(date) & models.Activity.user_id == user_id
        )
        .all()
    )


# Функция для получения всех активностей по типу и дате
def get_activities_by_time_date(
    db: Session, user_id: int, type: str, date: str
):
    type = (
        db.query(models.ActivityType)
        .filter(models.ActivityType.name == type)
        .first()
    )
    return (
        db.query(models.Activity)
        .filter(
            models.Activity.start_time.contains(date) & (
                models.Activity.user_id == user_id and models.Activity.type_id == type.id
            )
        ).all()
    )


# Функция для получения активности по её идентификатору
def get_activity(db: Session, activity_id: int):
    return (
        db.query(models.Activity)
        .filter(models.Activity.id == activity_id)
        .first()
    )


# Функция для создания новой активности // TODO
def create_activity(db: Session, activity: schemas.ActivityCreate):
    db_activity = models.Activity(**activity.dict())
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity


# Функция для обновления данных активности // TODO
def update_activity(
    db: Session, activity_id: int, activity: schemas.ActivityUpdate
):
    db_activity = (
        db.query(models.Activity)
        .filter(models.Activity.id == activity_id)
        .first()
    )
    if db_activity:
        for key, value in activity.dict().items():
            setattr(db_activity, key, value)
        db.commit()
        db.refresh(db_activity)
    return db_activity


# Функция для удаления активности
def delete_activity(db: Session, activity_id: int):
    db_activity = (
        db.query(models.Activity)
        .filter(models.Activity.id == activity_id)
        .first()
    )
    if db_activity:
        db.delete(db_activity)
        db.commit()
        return {"message": "Activity deleted successfully"}
    else:
        return {"message": "Activity not found"}
