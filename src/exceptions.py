from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi import status

from src.schemas import ErrorResponse

async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    reasons = [error["msg"] for error in exc.errors()]
    combined = " ".join(set(reasons))
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=ErrorResponse(reason=combined).model_dump(),
    )

async def http409_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content=ErrorResponse(reason=exc.detail).model_dump(),
    )

async def http401_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=ErrorResponse(reason=exc.detail).model_dump(),
    )
