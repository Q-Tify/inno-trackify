from sqlalchemy.orm import Session
from .. import models
from ..schemas import activities as schemas


# Функция для получения всех активностей
def get_activities(db: Session):
    return db.query(models.Activity).all()


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
