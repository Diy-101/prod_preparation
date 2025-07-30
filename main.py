from fastapi import FastAPI, HTTPException
from src.routers import main_router
from src.database import engine, Base
from src.exceptions import (
    validation_exception_handler,
    http409_handler,
    http401_handler
)
from fastapi.exceptions import RequestValidationError
import src.user.models
import src.country.models

app = FastAPI()
app.include_router(main_router)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(409, http409_handler)
app.add_exception_handler(401, http401_handler)

Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080)