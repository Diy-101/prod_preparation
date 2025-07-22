from sqlalchemy.orm import Session
from sqlalchemy import select
from src.database.models import Country

async def select_all_countries(db: Session, region: list | None = None):
    stmt = select(Country)

    if region is not None:
        stmt = stmt.where(Country.region.in_(region))

    countries_result = db.execute(stmt).scalars().all()
    for country in countries_result:
        if hasattr(country, "region") and isinstance(country.region, str):
            country.region = country.region.strip()
            if country.region == "":
                country.region = None
    return countries_result