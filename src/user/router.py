from fastapi import (
    APIRouter,
    Depends,
    Body,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session
from typing import Annotated
from src.database import get_db
import src.user.schemas as schemas, src.user.models as models
import src.user.utils as utils

user_router = APIRouter()

@user_router.post(
    "/api/auth/register",
    tags=["user"],
    summary="Регистрация нового пользователя",
    description="Используется для регистрации нового пользователя по логину и паролю",
    status_code=status.HTTP_201_CREATED,
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
) -> schemas.UserProfileRegistered:
    data = user_data.model_dump(mode="python", exclude_none=True)

    if data.get("image", None) is not None:
        data["image"] = data["image"].unicode_string()

    # Check for existence
    if data.get("phone", None) is not None:
        query = db.query(models.User).filter(
            (models.User.email == data["email"]) |
            (models.User.login == data["login"]) |
            (models.User.phone == data["phone"])
        ).first()
    else:
        query = db.query(models.User).filter(
            (models.User.email == data["email"]) |
            (models.User.login == data["login"])
        ).first()

    if query is not None:
        raise HTTPException(
            status_code=409,
            detail=f"Пользователь с таким данными уже существует"
        )

    # Creating new user
    hashed_password = utils.get_password_hash(user_data.password)

    new_user = models.User(
        login=data["login"],
        email=data["email"],
        countryCode=data["countryCode"],
        isPublic=data["isPublic"],
        phone=data["phone"] if data.get("phone", None) else None,
        image=data["image"] if data.get("image", None) else None,
        hashed_password=hashed_password,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return schemas.UserProfileRegistered(profile=data)

@user_router.post(
    "/api/auth/sign-in",
    tags=["user"],
    summary="Аутентификация для получения токена",
    description="Роутер для получения токена пользователем для дальнейшей авторизации",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Возвращает токен пользователя",
            "content": {
                "application/json": {
                    "example": {
                        "token": "<KEY>"
                    }
                }
            }
        }
    }
)
async def sign_up_user(
        user_data: Annotated[schemas.UserSignIn, Body(
            description="Данные для аутентификации пользователя.",
            examples=[
                {
                    "login": "yellowMonkey",
                    "password": "$aba4821FWfew01#.fewA$",
                }
            ]
        )
        ],
        db: Session = Depends(get_db)
) -> schemas.Token:
    query = db.query(models.User).filter(models.User.login == user_data.login).first()
    if query is None or not utils.verify_password(user_data.password, query.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Пользователь с указанным логином и паролем не найден",
            headers={"WWW-Authenticate": "Bearer"}
        )
    token = utils.create_access_token(data={"sub": query.login})
    return schemas.Token(token=token)

@user_router.get(
    "/api/me/profile",
    tags=["user"],
    summary="Получение собственного профиля",
    description="Используется для получения пользователем его собственного профиля.",
    response_model_exclude_none=True,
)
async def get_user_profile(
        user_profile: schemas.UserProfile = Depends(utils.get_profile_via_token)
) -> schemas.UserProfile:
    return user_profile
