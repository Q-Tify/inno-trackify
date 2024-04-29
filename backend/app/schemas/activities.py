from pydantic import BaseModel


# Схема для входных данных активностей
class ActivityBase(BaseModel):
    name: str
    type_id: int


# Схема для создания активностей
class ActivityCreate(ActivityBase):
    user_id: int
    start_time: str
    end_time: str
    duration: str
    description: str


# Схема для обновления активностей
class ActivityUpdate(ActivityBase):
    pass


# Схема для возвращаемых данных активностей
class Activity(ActivityBase):
    id: int
    user_id: int
    start_time: str
    end_time: str
    duration: str
    description: str

    class Config:
        orm_mode = True
