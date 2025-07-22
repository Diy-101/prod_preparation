from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.schemas.country import Country
from src.dependencies import get_db
from src.database.crud import select_all_countries
country_router = APIRouter()


@country_router.get("/api/countries", tags=["Country"], summary="Get all countries from database", response_model=list[Country])
async def get_countries(db: Session = Depends(get_db)):
    result = await select_all_countries(db)
    return result

@country_router.post("/api/countries/{alpha2}", tags=["Country"], summary="Get one country from database via alpha2", response_model=list[Country])
def add_country(name: str):
    return {"ok": True}