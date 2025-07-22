from pydantic import BaseModel, Field

class ErrorResponse(BaseModel):
    reason: str = Field(..., min_length=5)