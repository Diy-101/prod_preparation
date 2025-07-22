from sqlalchemy.orm import Session
from sqlalchemy import select
from src.database.models import country

async def get_countries(db: Session):
    stmt = select(country)
    countries = db.execute(stmt).scalars().all()
    return countries