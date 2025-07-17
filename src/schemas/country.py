from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Literal, Annotated

class CountryAlpha2(BaseModel):
    alpha2: str = Field(...,
                        max_length=2,
                        pattern="^[a-zA-Z]{2}$",
                        examples=["RU"],
                        description="Двухбуквенный код, уникально идентифицирующий страну")

class CountryRegion(BaseModel):
    country: Literal["Europe", "Africa", "Americas", "Oceania", "Asia"] = Field(..., description="Географический регион, к которому относится страна")

class Country(BaseModel):
    name: str = Field(..., max_length=100, description="Полное название страны")
    alpha2: CountryAlpha2
    alpha3: str = Field(...,
                        max_length=3,
                        pattern="^[a-zA-Z]{3}$",
                        description="Трехбуквенный код страны")
    region: Optional[CountryRegion] = None