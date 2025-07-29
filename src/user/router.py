from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from src.database import get_db
import src.user.schemas as schemas, src.user.models as models

user_router = APIRouter()

@user_router.post(
    "/auth/register",
    tags=["users"],
    summary="Регистрация нового пользователя",
    description="Используется для регистрации нового пользователя по логину и паролю",
    response_model=schemas.UserProfile,
    responses={
        201: {
            "description": "В случае успеха возвращается профиль зарегистрированного пользователя",
            "content": {
                "application/json": {
                    "example": {
                        "profile": {
                            "login": "yellowMonkey",
                            "email": "yellowstone1980@you.ru",
                            "countryCode": "RU",
                            "isPublic": True,
                            "phone": "+74951239922",
                            "image": "https://http.cat/images/100.jpg"
                        }
                    }
                }
            }
        },
        400: {
            "description": "Регистрационные данные не соответствуют ожидаемому формату и требованиям.",
            "content": {
                "application/json": {
                    "example": {
                        {
                        "reason": "<объяснение, почему запрос пользователя не может быть обработан>"
                        }
                    }
                }
            }
        },
        409: {
            "description": "Нарушено требование на уникальность авторизационных данных пользователей.",
            "content": {
                "application/json": {
                    "example": {
                        {
                        "reason": "<объяснение, почему запрос пользователя не может быть обработан>"
                        }
                    }
                }
            }
        }
    }
)
async def register_user(
        user_data: Annotated[
            schemas.UserRegistration,
            Body(
                description="Данные для регистрации пользователя.",
                examples=[
                    {
                    "login": "yellowMonkey",
                    "email": "yellowstone1980@you.ru",
                    "password": "$aba4821FWfew01#.fewA$",
                    "countryCode": "RU",
                    "isPublic": True,
                    "phone": "+74951239922",
                    "image": "https://http.cat/images/100.jpg"
                    }
                ]
            )
        ],
        db: Session = Depends(get_db)
):
    query: models.User | None
    for check in ["login", "email", "phone"]:
        query = db.query(models.User).filter(getattr(models.User, check) == user_data[check]).first()
        if query is not None:
            raise HTTPException(
                status_code=409,
                detail=f"Пользователь с таким {check} уже существует"
            )
    return