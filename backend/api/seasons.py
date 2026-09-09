from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db
from models.season import Season
from schemas.season import SeasonOut

router = APIRouter()


@router.get("/", response_model=list[SeasonOut])
async def list_seasons(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Season).order_by(Season.year.desc()))
    return result.scalars().all()


@router.get("/current", response_model=SeasonOut)
async def current_season(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Season).where(Season.current == True))
    season = result.scalar_one_or_none()
    if not season:
        result = await db.execute(select(Season).order_by(Season.year.desc()))
        season = result.scalars().first()
    return season
