from fastapi import APIRouter

router = APIRouter()

# Healthcheck
@router.get("/healthz")
def healthz():
    return {"service": "Activity Tracker", "status": "ok"}

@router.get("/")
def healthz():
    return {"service": "Activity Tracker", "status": "ok"}