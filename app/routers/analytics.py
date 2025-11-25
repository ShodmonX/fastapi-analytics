from fastapi import APIRouter, Depends, Body, Query, status
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from app.db import get_db
from app.schemas import EventCreate, EventOut
from app.crud import analytics as crud

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)

@router.get("/", response_model=list[EventOut])
async def get_activities(
    skip: int = Query(0, ge=0),
    limit: int = Query(1000, ge=1, le=10000),
    db: AsyncSession = Depends(get_db)
):
    return await crud.get_activities(db, skip, limit)


@router.post("/", response_model=EventOut, status_code=status.HTTP_201_CREATED)
async def add_activity(
    event: Annotated[EventCreate, Body()],
    db: AsyncSession = Depends(get_db)
):
    return await crud.add_activity(db, event)

@router.get("/users/{user_id}/", response_model=list[EventOut])
async def get_user_activity(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    start: datetime | None = None,
    end: datetime | None = None,
    event_type: str | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
):
    return await crud.get_user_activities_in_period(
        db=db,
        user_id=user_id,
        limit=limit,
        start=start,
        end=end,
        event_type=event_type,
        skip=skip
    )

@router.get("/stats/")
async def stats(days: int = Query(30, ge=1, le=365), db: AsyncSession = Depends(get_db)):
    dau = await crud.get_unique_users_last_n_days(db, days=1)
    wau = await crud.get_unique_users_last_n_days(db, days=7)
    mau = await crud.get_unique_users_last_n_days(db, days=days)
    total = await crud.get_total_events(db)
    return {"dau": dau, "wau": wau, "mau": mau, "total_events": total, "period_days": days}

@router.get("/top-events/")
async def top_events(days: int = Query(7, ge=1, le=365), limit: int = Query(10, ge=1, le=100), db: AsyncSession = Depends(get_db)):
    return await crud.get_top_events(db, days=days, limit=limit)

@router.get("/users/{user_id}/last-seen/")
async def last_seen(user_id: int, db: AsyncSession = Depends(get_db)):
    last = await crud.get_user_last_seen(db, user_id)
    return {"user_id": user_id, "last_seen": last.isoformat() if last else None}
