import hashlib
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from .. import models
from ..schemas import authentication as schemas
from ..schemas import users as user_schemas
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from ..config import SECRET_KEY, ALGORITHM, EXPIRE_TIME_MINUTES


def get_user_username_password(db: Session, username: str, password: str):
    return (
        db.query(models.User)
        .filter(
            models.User.username == username, models.User.password == password
        )
        .first()
    )


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=EXPIRE_TIME_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_username_from_token(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    return payload.get("sub")