from pydantic import BaseModel, RootModel, Field, EmailStr, HttpUrl, field_validator
from typing import Optional, Literal, Annotated
from src.schemas import CountryAlpha2
import re

class UserLogin(RootModel[Annotated[str, Field(
    max_length=30,
    pattern="[a-zA-Z0-9-]+",
    examples=["yellowMonkey"],
    description="Логин пользователя"
)]]):
    pass

class UserEmail(RootModel[Annotated[EmailStr, Field(
    max_length=50,
    min_length=1,
    examples=["yellowstone1980@you.ru"],
    description="E-mail пользователя"
)]]):
    pass

class UserPassword(RootModel[Annotated[str, Field(
    max_length=100,
    min_length=6,
    description="""
    Пароль пользователя, к которому предъявляются следующие требования:
        - Длина пароля не менее 6 символов.
        -Присутствуют латинские символы в нижнем и верхнем регистре.
        - Присутствует минимум одна цифра.
    """
)]]):
    pass

class UserIsPublic(RootModel[Annotated[bool, Field(
    examples=["true"],
    description="Публичные профили доступны другим пользователям: если профиль публичный, \
    любой пользователь платформы сможет получить информацию о пользователе."
)]]):
    pass

class UserPhone(RootModel[Annotated[str, Field(
    max_length=20,
    pattern=r"\+[\d]+",
    examples=["example: +74951239922"],
    description="Номер телефона пользователя в формате +123456789"
)]]):
    pass

class UserImage(RootModel[Annotated[HttpUrl, Field(
    max_length=200,
    min_length=1,
    description="Ссылка на фото для аватара пользователя"
)]]):
    pass

class UserProfile(BaseModel):
    login: UserLogin
    email: UserEmail
    countryCode: CountryAlpha2
    isPublic: UserIsPublic
    phone: UserPhone | None = None
    image: UserImage | None = None

class UserRegistration(UserProfile):
    password: UserPassword

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