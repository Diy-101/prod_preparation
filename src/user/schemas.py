from pydantic import (
    BaseModel,
    Field, EmailStr,
    HttpUrl, ConfigDict,
    field_validator
)

import re
from typing import Annotated

from src.schemas import CountryAlpha2


user_login = Annotated[str, Field(
    max_length=30,
    pattern="[a-zA-Z0-9-]+",
    examples=["yellowMonkey"],
    description="Логин пользователя"
)]
user_email = Annotated[EmailStr, Field(
    max_length=50,
    min_length=1,
    examples=["yellowstone1980@you.ru"],
    description="E-mail пользователя"
)]
user_password = Annotated[str, Field(
    max_length=100,
    min_length=6,
    description="""
    Пароль пользователя, к которому предъявляются следующие требования:
        - Длина пароля не менее 6 символов.
        -Присутствуют латинские символы в нижнем и верхнем регистре.
        - Присутствует минимум одна цифра.
    """
)]
user_is_public = Annotated[bool, Field(
    examples=["true"],
    description="Публичные профили доступны другим пользователям: если профиль публичный, \
    любой пользователь платформы сможет получить информацию о пользователе."
)]
user_phone = Annotated[str, Field(
    max_length=20,
    pattern=r"\+[\d]+",
    examples=["example: +74951239922"],
    description="Номер телефона пользователя в формате +123456789"
)]
user_image = Annotated[HttpUrl, Field(
    max_length=200,
    min_length=1,
    description="Ссылка на фото для аватара пользователя"
)]

class UserProfile(BaseModel):
    login: user_login
    email: user_email
    countryCode: CountryAlpha2
    isPublic: user_is_public
    phone: user_phone | None = None
    image: user_image | None = None

    model_config = ConfigDict(
        from_attributes=True,
    )

class UserRegistration(UserProfile):
    password: user_password

    @field_validator("password", mode="after")
    @classmethod
    def validate_password(cls, field: str) -> str:
        field = str(field)
        if not re.search(r"[a-z]", field):
            raise ValueError("Пароль должен содержать строчные латинские буквы.")
        if not re.search(r"[A-Z]", field):
            raise ValueError("Пароль должен содержать заглавные латинские буквы.")
        if not re.search(r"\d", field):
            raise ValueError("Пароль должен содержать хотя бы одну цифру.")
        return field

class UserProfileRegistered(BaseModel):
    profile: dict[str, str | None | bool]

class UserProfileUpdate(BaseModel):
    login: user_login | None = None
    email: user_email | None = None
    countryCode: CountryAlpha2 | None = None
    isPublic: user_is_public | None = None
    phone: user_phone | None = None
    image: user_image | None = None

    model_config = ConfigDict(
        from_attributes=True,
    )

class UserSignIn(BaseModel):
    login: user_login
    password: user_password

class Token(BaseModel):
    token: str