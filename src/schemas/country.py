from typing import Annotated, Literal

from pydantic import BaseModel, Field
from enum import StrEnum
from typing import Optional

CountryRegion = Annotated[str,
    Field(
        default=None,
        description="Географический регион, к которому относится страна",
        examples=["Europe", "Asia"]
    )
]

CountryAlpha2 = Annotated[
    str,
    Field(
        ...,
        max_length=2,
        pattern="^[A-Z]{2}$",
        examples=["RU"],
        description="Двухбуквенный код, уникально идентифицирующий страну"
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