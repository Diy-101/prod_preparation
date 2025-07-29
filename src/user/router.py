from fastapi import APIRouter
from src.dependencies import oauth2_scheme
from sqlalchemy.sql.annotation import Annotated

user_router = APIRouter()

@user_router.get("/users", tags=["users"], summary="Get all users")
async def get_all_users(token: Annotated[str, oauth2_scheme]):
    return {"token": token}