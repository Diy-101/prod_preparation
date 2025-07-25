from fastapi import APIRouter

from src.default.router import default_router
from src.user.router import user_router
from src.country.router import country_router

main_router = APIRouter()
main_router.include_router(default_router)
main_router.include_router(user_router)
main_router.include_router(country_router)