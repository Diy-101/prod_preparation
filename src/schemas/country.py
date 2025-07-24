from typing import Annotated, Literal
from pydantic import BaseModel, Field, field_validator

class Country(BaseModel):
    name: str = Field(..., max_length=100, description="Полное название страны")
    alpha2: str = Field(...,
                        min_length=2,
                        max_length=2,
                        pattern="^[a-zA-Z]{2}$",
                        description="Двухбуквенный код страны")
    alpha3: str = Field(...,
                        min_length=3,
                        max_length=3,
                        pattern="^[a-zA-Z]{3}$",
                        description="Трехбуквенный код страны")
    region: Literal["Europe", "Africa", "Americas", "Oceania", "Asia"] | None = None