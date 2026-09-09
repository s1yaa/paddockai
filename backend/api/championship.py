from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database import get_db
from models.standing import DriverStanding, ConstructorStanding
from models.season import Season

router = APIRouter()


@router.get("/drivers")
async def driver_championship(
    season_year: int | None = None,
    db: AsyncSession = Depends(get_db),
):
    season_id = await _get_season_id(db, season_year)
    if not season_id:
        return []

    result = await db.execute(
        select(DriverStanding)
        .options(
            selectinload(DriverStanding.driver).selectinload(
                __import__("models.driver", fromlist=["Driver"]).Driver.constructor
            ),
            selectinload(DriverStanding.constructor),
        )
        .where(DriverStanding.season_id == season_id)
        .order_by(DriverStanding.position)
    )
    standings = result.scalars().all()

    return [
        {
            "id": str(s.id),
            "position": s.position,
            "points": float(s.points),
            "wins": s.wins,
            "podiums": s.podiums,
            "poles": s.poles,
            "dnfs": s.dnfs,
            "races_entered": s.races_entered,
            "driver": {
                "id": str(s.driver.id),
                "slug": s.driver.slug,
                "name": f"{s.driver.first_name} {s.driver.last_name}",
                "abbreviation": s.driver.abbreviation,
                "number": s.driver.number,
                "nationality": s.driver.nationality,
            },
            "constructor": {
                "id": str(s.constructor.id) if s.constructor else None,
                "name": s.constructor.name if s.constructor else None,
                "slug": s.constructor.slug if s.constructor else None,
                "color": s.constructor.color_primary if s.constructor else None,
            } if s.constructor else None,
        }
        for s in standings
    ]


@router.get("/constructors")
async def constructor_championship(
    season_year: int | None = None,
    db: AsyncSession = Depends(get_db),
):
    season_id = await _get_season_id(db, season_year)
    if not season_id:
        return []

    result = await db.execute(
        select(ConstructorStanding)
        .options(selectinload(ConstructorStanding.constructor))
        .where(ConstructorStanding.season_id == season_id)
        .order_by(ConstructorStanding.position)
    )
    standings = result.scalars().all()

    return [
        {
            "id": str(s.id),
            "position": s.position,
            "points": float(s.points),
            "wins": s.wins,
            "podiums": s.podiums,
            "constructor": {
                "id": str(s.constructor.id),
                "name": s.constructor.name,
                "slug": s.constructor.slug,
                "color": s.constructor.color_primary,
            },
        }
        for s in standings
    ]


async def _get_season_id(db: AsyncSession, year: int | None):
    if year:
        result = await db.execute(select(Season).where(Season.year == year))
    else:
        result = await db.execute(select(Season).where(Season.current == True))
    season = result.scalar_one_or_none()
    if not season and not year:
        result = await db.execute(select(Season).order_by(Season.year.desc()))
        season = result.scalars().first()
    return season.id if season else None
