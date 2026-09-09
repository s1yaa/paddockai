from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database import get_db
from models.race import Race
from models.season import Season
from models.session import Session as RaceSession
from schemas.race import RaceListItem, RaceDetail

router = APIRouter()


@router.get("/", response_model=list[RaceListItem])
async def list_races(
    season_year: int | None = None,
    db: AsyncSession = Depends(get_db),
):
    query = (
        select(Race)
        .options(selectinload(Race.circuit))
        .order_by(Race.date)
    )
    if season_year:
        result = await db.execute(select(Season).where(Season.year == season_year))
        season = result.scalar_one_or_none()
        if season:
            query = query.where(Race.season_id == season.id)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/next", response_model=RaceListItem)
async def next_race(db: AsyncSession = Depends(get_db)):
    today = date.today()
    result = await db.execute(
        select(Race)
        .options(selectinload(Race.circuit))
        .where(Race.date >= today)
        .order_by(Race.date)
    )
    race = result.scalars().first()
    if not race:
        raise HTTPException(status_code=404, detail="No upcoming races found")
    return race


@router.get("/{race_id}", response_model=RaceDetail)
async def get_race(race_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Race)
        .options(
            selectinload(Race.circuit),
            selectinload(Race.sessions),
        )
        .where(Race.id == race_id)
    )
    race = result.scalar_one_or_none()
    if not race:
        raise HTTPException(status_code=404, detail="Race not found")
    return race


@router.get("/{race_id}/status")
async def race_status(race_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Race)
        .options(selectinload(Race.sessions))
        .where(Race.id == race_id)
    )
    race = result.scalar_one_or_none()
    if not race:
        raise HTTPException(status_code=404, detail="Race not found")

    sessions = {s.session_type: s.status for s in race.sessions}
    return {
        "race_id": str(race.id),
        "gp_name": race.gp_name,
        "status": race.status,
        "sessions": sessions,
        "current_stage": _determine_stage(sessions),
    }


def _determine_stage(sessions: dict[str, str]) -> str:
    order = ["fp1", "fp2", "fp3", "qualifying", "race"]
    for s in order:
        if sessions.get(s) in ("upcoming", None):
            return s
    return "completed"
