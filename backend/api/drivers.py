from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database import get_db
from models.driver import Driver
from schemas.driver import DriverOut

router = APIRouter()


@router.get("/", response_model=list[DriverOut])
async def list_drivers(
    active_only: bool = True,
    db: AsyncSession = Depends(get_db),
):
    query = (
        select(Driver)
        .options(selectinload(Driver.constructor))
        .order_by(Driver.last_name)
    )
    if active_only:
        query = query.where(Driver.active == True)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{driver_id}", response_model=DriverOut)
async def get_driver(driver_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Driver)
        .options(selectinload(Driver.constructor))
        .where(Driver.id == driver_id)
    )
    driver = result.scalar_one_or_none()
    if not driver:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Driver not found")
    return driver
