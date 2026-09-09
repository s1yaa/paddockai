"""
PaddockAI Backend — FastAPI Application
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from database import engine, Base
from api import seasons, races, drivers, constructors, championship, data


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup if they don't exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(
    title="PaddockAI API",
    description="F1 Prediction Intelligence Platform — Backend API",
    version="1.0.0",
    lifespan=lifespan,
)

# ── CORS ─────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(seasons.router,      prefix="/api/seasons",       tags=["Seasons"])
app.include_router(races.router,        prefix="/api/races",         tags=["Races"])
app.include_router(drivers.router,      prefix="/api/drivers",       tags=["Drivers"])
app.include_router(constructors.router, prefix="/api/constructors",  tags=["Constructors"])
app.include_router(championship.router, prefix="/api/championship",  tags=["Championship"])
app.include_router(data.router,         prefix="/api/data",          tags=["Data"])


@app.get("/health", tags=["Health"])
async def health():
    return {
        "status": "ok",
        "version": "1.0.0",
        "app": "PaddockAI",
    }
