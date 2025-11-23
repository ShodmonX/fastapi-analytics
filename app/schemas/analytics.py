from pydantic import BaseModel, Field, ConfigDict, field_validator
from datetime import datetime


from enum import StrEnum

class EventPrefix(StrEnum):
    # Auth
    LOGIN = "login"
    LOGOUT = "logout"
    SIGNUP = "signup"
    
    # Content
    POST = "post"
    COMMENT = "comment"
    
    # App
    APP = "app"
    SESSION = "session"
    PAGE = "page_view"
    SCREEN = "screen_view"
    
    # User actions
    PROFILE = "profile"
    SEARCH = "search"
    NOTIFICATION = "notification"
    
    # Business
    ONBOARDING = "onboarding"
    FEATURE = "feature"
    PAYMENT = "payment"
    SUBSCRIPTION = "subscription"

class EventCreate(BaseModel):
    user_id: int = Field(..., gt=0, examples=[123, 456])
    event_type: str = Field(..., min_length=1, max_length=50, examples=["login", "logout", "register"])

    @field_validator('event_type', mode="before")
    def validate_event_type(cls, v):
        if not any(v.startswith(prefix) for prefix in EventPrefix):
            raise ValueError(f"event_type must start with one of: {', '.join(EventPrefix)}")
        return v

class EventOut(BaseModel):
    id: int
    user_id: int
    event_type: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)