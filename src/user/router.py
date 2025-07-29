from fastapi import APIRouter

user_router = APIRouter()

@user_router.get("/users", tags=["users"], summary="Get all users")
async def get_all_users(token: str):
    return {"token": token}