from pydantic import BaseModel, Field, RootModel
from typing import Annotated, Literal

class CountryAlpha2(RootModel[Annotated[str,  Field(
    pattern="^[a-zA-Z]{2}$",
    description="Двухбуквенный код страны"
)]]):
    pass

class ErrorResponse(BaseModel):
    reason: str = Field(..., min_length=5)