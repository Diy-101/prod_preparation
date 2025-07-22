from sqlalchemy.orm import Session
from sqlalchemy import select
async def get_countries(db: Session):
    select()