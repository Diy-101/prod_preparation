from fastapi import APIRouter
default_router = APIRouter()

@default_router.get("/api/ping", tags=['default'])
def ping():
    return {"ok": True}