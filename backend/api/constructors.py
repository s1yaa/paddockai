from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db
from models.constructor import Constructor
from schemas.constructor import ConstructorOut

router = APIRouter()


@router.get("/", response_model=list[ConstructorOut])
async def list_constructors(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Constructor).order_by(Constructor.name)
    )
    return result.scalars().all()


@router.get("/{constructor_id}", response_model=ConstructorOut)
async def get_constructor(constructor_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Constructor).where(Constructor.id == constructor_id)
    )
    c = result.scalar_one_or_none()
    if not c:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Constructor not found")
    return c
