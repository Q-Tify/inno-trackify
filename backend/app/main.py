from fastapi import FastAPI
from .api import activities, users, authentication, healthz
from .config import GIT_INFO

app = FastAPI(description=f"Activity Tracker API<br>{GIT_INFO}")

# Подключаем роуты для активностей и пользователей
app.include_router(activities.router)
app.include_router(users.router)
app.include_router(authentication.router)
app.include_router(healthz.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8000)
