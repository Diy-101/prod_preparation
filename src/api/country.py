from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.schemas.country import Country
from src.dependencies import get_db

country_router = APIRouter()


@country_router.get("/api/countries", tags=["start"], summary="Get all countries from database", response_model=list[Country])
def get_countries(db: Session = Depends(get_db)):

    return

@country_router.post("/api/countries/{alpha2}", tags=["start"], summary="Add one schemas to database")
def add_country(name: str):
    return {"ok": True}