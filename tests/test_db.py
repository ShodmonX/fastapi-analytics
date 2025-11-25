from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient

from app.crud import analytics as crud
from app.schemas import EventCreate


async def test_database(test_db: AsyncSession, client: AsyncClient):
    result = await test_db.execute(select(1))
    assert result.scalar() == 1

    activity = await crud.add_activity(test_db, EventCreate(event_type="login", user_id=1))
    assert activity.event_type == "login"
    assert activity.user_id == 1

    acticity = await crud.get_activities(test_db)
    assert len(acticity) == 1
    
    count = await crud.get_unique_users_last_n_days(test_db, 1)
    assert count == 1

    activity = await crud.get_user_activities_in_period(test_db, user_id=1, limit=1)
    assert activity
    assert len(activity) == 1

    activity = await crud.get_top_events(test_db)
    assert activity
    assert len(activity) == 1
    assert activity[0]["event_type"] == "login"
    assert activity[0]["count"] == 1

    activity = await crud.get_user_last_seen(test_db, user_id=1)
    assert activity

    activity = await crud.get_total_events(test_db)
    assert activity
    assert activity == 1