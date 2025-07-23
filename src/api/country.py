from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import Field
from sqlalchemy.orm import Session
from typing import List, Annotated
from src.schemas.country import Country
from src.dependencies import get_db
from src.database.crud import select_countries, select_alpha2
from src.schemas.error import ErrorResponse

country_router = APIRouter()

@country_router.get(
    "/api/countries",
    tags=["Country"],
    summary="Get all countries from database",
    response_model=List[Country],
    responses={
        400: {
            "description": "Формат входного запроса не соответствует формату либо переданы неверные значения.",
            "model": ErrorResponse,
            "content": {
                "application/json": {
                    "example": {
                        "reason": "<объяснение, почему запрос пользователя не может быть обработан>",
                    }
                }
            }
        },
    },
)
def get_countries(
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
        result = select_countries(db, region=region)
    except Exception as e:
        raise HTTPException(status_code=400, detail={"reason": str(e)})
    return result

@country_router.get(
    "/api/countries/{alpha2}",
    tags=["Country"],
    summary="Get one country from database via alpha2",
    response_model=Country,
    responses={
    404: {
        "description": "Страна с данным alpha2 не найдена",
        "model": ErrorResponse,
        "content": {
            "application/json": {
                "example": {
                    "reason": "<объяснение, почему запрос пользователя не может быть обработан>"
                }
            }
        }
    }
}
)
def get_alpha2(
        alpha2: Annotated[str, Field(..., max_length=2, pattern=r"[A-Z]{2}", description="Возвращаемая страна должна иметь указанный alpha2 код.")],
        db: Session = Depends(get_db),
):
    result = select_alpha2(db, alpha2=alpha2)
    if result is None:
        raise HTTPException(status_code=404, detail="Страна с данным alpha2 не найдена")
    return result