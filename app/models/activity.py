from sqlalchemy import Integer, String, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from datetime import datetime

from app.db import Base


class ActivityLog(Base):
    __tablename__ = 'activity_logs'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, index=True, nullable=False)
    event_type: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True, nullable=False)

    __table_args__ = (
        Index('ix_activity_user_created', user_id, created_at.desc()),
        Index('ix_activity_type_created', event_type, created_at.desc()),
        Index('ix_activity_date', created_at.desc()),
    )