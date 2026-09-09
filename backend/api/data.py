"""
Data ingestion endpoints — Phase 2 will flesh these out fully.
Phase 1: stubs that return 200 OK so the frontend can reference them.
"""
from fastapi import APIRouter

router = APIRouter()


@router.post("/practice")
async def add_practice():
    return {"status": "not_implemented", "message": "Data entry coming in Phase 2"}


@router.post("/qualifying")
async def add_qualifying():
    return {"status": "not_implemented", "message": "Data entry coming in Phase 2"}


@router.post("/race")
async def add_race():
    return {"status": "not_implemented", "message": "Data entry coming in Phase 2"}


@router.post("/upload")
async def upload_csv():
    return {"status": "not_implemented", "message": "CSV upload coming in Phase 2"}


@router.post("/refresh")
async def refresh_data():
    return {"status": "not_implemented", "message": "Live data refresh coming in Phase 11"}
