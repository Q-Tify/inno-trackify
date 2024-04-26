from fastapi import FastAPI
from .api import activities, users, authentication

app = FastAPI()

# Подключаем роуты для активностей и пользователей
app.include_router(activities.router)
app.include_router(users.router)
app.include_router(authentication.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
