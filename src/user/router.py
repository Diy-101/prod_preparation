from fastapi import APIRouter
from sqlalchemy.sql.annotation import Annotated

user_router = APIRouter()

@user_router.get("/users", tags=["users"], summary="Get all users")
async def get_all_users(token: Annotated[str]):
    return {"token": token}