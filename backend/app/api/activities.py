from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from ..crud import activities as crud
from ..schemas import activities as schemas
from ..schemas import users as users_schemas
from ..database import SessionLocal
from ..api.authentication import authenticate_user, oauth2_scheme

router = APIRouter()


# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Dependency to get current active user
def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    user = authenticate_user(db, token)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


# Route to fetch all activities
@router.get("/activities/", response_model=List[schemas.Activity])
def get_activities(
    db: Session = Depends(get_db),
    current_user: users_schemas.User = Depends(get_current_user),
):
    return crud.get_activities(db, current_user.id)


# Route to fetch all activities
@router.put("/activities/", response_model=List[schemas.Activity])
def get_activities_params(
    type: str | None = None,
    date: str | None = None,
    db: Session = Depends(get_db),
    current_user: users_schemas.User = Depends(get_current_user),
):
    if type is None and date is None:
        return crud.get_activities(db, current_user.id)
    elif type is None:
        return crud.get_activities_by_date(db, current_user.id, date)
    elif date is None:
        return crud.get_activities_by_type(db, current_user.id, type)
    else:
        return crud.get_activities_by_time_date(
            db, current_user.id, type, date
        )


# Route to fetch a single activity by ID
@router.get("/activities/{activity_id}", response_model=schemas.Activity)
def get_activity(
    activity_id: int,
    db: Session = Depends(get_db),
    current_user: users_schemas.User = Depends(get_current_user),
):
    activity = crud.get_activity(db, activity_id)
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity


# Route to create a new activity
@router.post("/activities/", response_model=schemas.Activity)
def create_activity(
    activity: schemas.ActivityCreate,
    db: Session = Depends(get_db),
    current_user: users_schemas.User = Depends(get_current_user),
):
    return crud.create_activity(db, activity)


# Route to update an existing activity
@router.put("/activities/{activity_id}", response_model=schemas.Activity)
def update_activity(
    activity_id: int,
    activity: schemas.ActivityUpdate,
    db: Session = Depends(get_db),
    current_user: users_schemas.User = Depends(get_current_user),
):
    return crud.update_activity(db, activity_id, activity)


# Route to delete an activity
@router.delete("/activities/{activity_id}")
def delete_activity(
    activity_id: int,
    db: Session = Depends(get_db),
    current_user: users_schemas.User = Depends(get_current_user),
):
    return crud.delete_activity(db, activity_id)
