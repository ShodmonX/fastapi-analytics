from sqlalchemy import text, func
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from app.models import ActivityLog
from app.schemas import EventCreate

async def add_activity(db: AsyncSession, event: EventCreate) -> ActivityLog:
    activity = ActivityLog(user_id=event.user_id, event_type=event.event_type)
    try:
        db.add(activity)
        await db.commit()
        await db.refresh(activity)
        return activity
    except Exception:
        await db.rollback()
        raise

async def get_activities(db: AsyncSession, skip: int = 0, limit: int = 1000) -> list[ActivityLog]:
    stm = select(ActivityLog).offset(skip).limit(limit)
    result = await db.execute(stm)
    return result.scalars().all()

async def get_unique_users_last_n_days(db: AsyncSession, days: int) -> int:
    """
    Use make_interval so we can pass integer `days` safely (asyncpg expects correct types).
    """
    result = await db.execute(
        text("""
            SELECT COUNT(DISTINCT user_id)
            FROM activity_logs
            WHERE created_at >= CURRENT_DATE - make_interval(days => :days)
        """),
        {"days": days}
    )
    return result.scalar() or 0

async def get_user_activities_in_period(
    db: AsyncSession,
    user_id: int,
    limit: int,
    start: datetime | None = None,
    end: datetime | None = None,
    event_type: str | None = None,
    skip: int = 0
) -> list[ActivityLog]:
    """
    Get activities for a user in a period (returns list of ActivityLog).
    """
    query = select(ActivityLog).where(ActivityLog.user_id == user_id)

    if start:
        query = query.where(ActivityLog.created_at >= start)
    if end:
        query = query.where(ActivityLog.created_at < end)
    if event_type:
        query = query.where(ActivityLog.event_type == event_type)
    if skip:
        query = query.offset(skip)

    query = query.limit(limit)

    result = await db.execute(query)
    return result.scalars().all()

async def get_top_events(db: AsyncSession, days: int = 7, limit: int = 10):
    """
    Return list of dicts: [{"event_type": "...", "count": n}, ...]
    Uses make_interval so `days` can be int.
    """
    result = await db.execute(
        text("""
            SELECT event_type, COUNT(*) as cnt 
            FROM activity_logs 
            WHERE created_at >= CURRENT_DATE - make_interval(days => :days)
            GROUP BY event_type 
            ORDER BY cnt DESC 
            LIMIT :limit
        """),
        {"days": days, "limit": limit}
    )
    return [{"event_type": row[0], "count": row[1]} for row in result]

async def get_user_last_seen(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(func.max(ActivityLog.created_at)).where(ActivityLog.user_id == user_id)
    )
    return result.scalar()

async def get_total_events(db: AsyncSession):
    result = await db.execute(
        select(func.count()).select_from(ActivityLog)
    )
    return result.scalar() or 0
