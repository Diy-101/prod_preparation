from fastapi import FastAPI
from src.routers import main_router
from src.database import engine, Base
import src.user.models
import src.country.models

app = FastAPI()
app.include_router(main_router)

Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080)