from typing import Annotated, Literal

from pydantic import BaseModel, Field

class CountryAlpha2String(str):
    pass  # Можно добавить кастомную логику, но для OpenAPI достаточно аннотаций

CountryAlpha2 = Annotated[
    CountryAlpha2String,
    Field(
        min_length=2,
        max_length=2,
        pattern=r'^[A-Za-z]{2}$',
        example='RU',
        description='Двухбуквенный код, уникально идентифицирующий страну'
    )
]

class Country(BaseModel):
    name: str = Field(..., max_length=100, description="Полное название страны")
    alpha2: CountryAlpha2
    alpha3: str = Field(...,
                        max_length=3,
                        pattern="^[a-zA-Z]{3}$",
                        description="Трехбуквенный код страны")
    region: Literal["Europe", "Africa", "Americas", "Oceania", "Asia"] | None = None