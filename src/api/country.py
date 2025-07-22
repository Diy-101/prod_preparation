from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from src.schemas.country import Country
from src.dependencies import get_db
from src.database.crud import select_all_countries
from src.schemas.error import ErrorResponse

country_router = APIRouter()


@country_router.get(
    "/api/countries",
    tags=["Country"],
    summary="Get all countries from database",
    response_model=List[Country],
    responses={
        400: {
            "description": "Bad Request",
            "model": ErrorResponse,
            "content": {
                "application/json": {
                    "example": {
                        "reason": "Формат входного запроса не соответствует формату либо переданы неверные значения.",
                    }
                }
            }
        },
    },
)
async def get_countries(
    region: List[str] = Query(
        None,
        description="Список регионов для фильтрации стран. Доступные значения: Europe, Africa, Americas, Oceania, Asia. "
                    "Если параметр отсутствует или передан пустой массив — фильтрация не применяется.",
        example=["Europe", "Asia"],
        enum=["Europe", "Africa", "Americas", "Oceania", "Asia"],
        title="Region Filter"
    ),
    db: Session = Depends(get_db)
):
    try:
        result = await select_all_countries(db, region=region)
    except Exception as e:
        raise HTTPException(status_code=400, detail={"reason": str(e)})
    return result

@country_router.post("/api/countries/{alpha2}", tags=["Country"], summary="Get one country from database via alpha2", response_model=list[Country])
def add_country(name: str):
    return {"ok": True}