from pydantic import BaseModel, Field, validator
from datetime import datetime, timezone
from .enums import EventStatus


class Event(BaseModel):
    id: str
    odds: float = Field(..., gt=0)
    deadline: datetime
    status: EventStatus = Field(...)


class UpdateEventResponse(BaseModel):
    event: Event
    message: str
    
class EventCreateRequest(BaseModel):
    odds: float = Field(..., example=2.5)  
    deadline: datetime = Field(..., example = datetime.now(timezone.utc))  


class EventResponse(BaseModel):
    id: str
    odds: float
    deadline: datetime
    status: EventStatus
