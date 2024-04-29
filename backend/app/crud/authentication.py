from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from . import users
from jose import jwt
from ..config import SECRET_KEY, ALGORITHM, EXPIRE_TIME_MINUTES
import bcrypt

def get_user_username_password(db: Session, username: str, password: str):
    user = users.get_user_by_username(db, username)
    if not user:
        return False
    if not bcrypt.checkpw(password.encode('utf-8'), user.password):
        return False
    return user


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
