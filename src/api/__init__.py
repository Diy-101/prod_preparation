from fastapi import APIRouter

from src.api.default import default_router
from src.api.user import user_router
from src.api.country import country_router

main_router = APIRouter()
main_router.include_router(default_router)
main_router.include_router(user_router)
main_router.include_router(country_router)