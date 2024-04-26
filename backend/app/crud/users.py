from sqlalchemy.orm import Session
from .. import models
from ..schemas import users as schemas
import re

# Функция для получения всех юзеров
def get_users(db: Session):
    return db.query(models.User).all()

# Функция для получения пользователя по его идентификатору
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# Функция для получения пользователя по его адресу электронной почты
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# Функция для получения пользователя по его имени
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

# Функция для проверки валидности адреса электронной почты
def validate_email(email: str):
    # Паттерн для проверки валидности адреса электронной почты
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email)

# Функция для создания нового пользователя
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email, password=user.password, username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Функция для обновления данных пользователя
def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        for key, value in user.dict().items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user

# Функция для удаления пользователя
def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return {"message": "User deleted successfully"}
    else:
        return {"message": "User not found"}
