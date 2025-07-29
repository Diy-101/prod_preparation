from fastapi import APIRouter, Depends, Body, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated
from src.database import get_db
import src.user.schemas as schemas, src.user.models as models
import src.user.utils as utils

user_router = APIRouter()

@user_router.post(
    "/api/auth/register",
    tags=["users"],
    summary="Регистрация нового пользователя",
    status_code=status.HTTP_201_CREATED,
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
                        "reason": "<объяснение, почему запрос пользователя не может быть обработан>"
                    }
                }
            }
        },
        409: {
            "description": "Нарушено требование на уникальность авторизационных данных пользователей.",
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
    # Check for existence
    for check in ["login", "email", "phone"]:
        if hasattr(user_data, check) and getattr(user_data, check):
            check_value = getattr(user_data, check)
            if hasattr(check_value, "root"):
                check_value = check_value.root

            query = db.query(models.User).filter(
                getattr(models.User, check) == check_value
            ).first()

            if query is not None:
                raise HTTPException(
                status_code=409,
                detail=f"Пользователь с таким {check} уже существует"
                )

    # Creating new user
    hashed_password = utils.get_password_hash(user_data.password)
    new_user = models.User(
        login=user_data.login,
        email=user_data.email,
        countryCode=user_data.countryCode,
        isPublic=user_data.isPublic,
        phone=user_data.phone,
        image=user_data.image,
        hashed_password=hashed_password,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return schemas.UserProfile(
        login=user_data.login,
        email=user_data.email,
        countryCode=user_data.countryCode,
        isPublic=user_data.isPublic,
        phone=user_data.phone,
        image=user_data.image,
    )