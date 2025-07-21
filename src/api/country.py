from fastapi import APIRouter
from src.schemas.country import Country
country_router = APIRouter()


@country_router.get("/api/countries", tags=["start"], summary="Get all countries from database", response_model=list[Country])
def get_countries():

    return

@country_router.post("/api/countries/{alpha2}", tags=["start"], summary="Add one schemas to database")
def add_country(name: str):
    return {"ok": True}