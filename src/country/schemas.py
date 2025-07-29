from pydantic import BaseModel, Field
from src.schemas import CountryAlpha2, CountryRegion

class Country(BaseModel):
    name: str = Field(..., max_length=100, description="Полное название страны")
    alpha2: CountryAlpha2
    alpha3: str = Field(...,
                        min_length=3,
                        max_length=3,
                        pattern="^[a-zA-Z]{3}$",
                        description="Трехбуквенный код страны")
    region: CountryRegion | None = None