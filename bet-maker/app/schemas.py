from pydantic import BaseModel, Field
from uuid import UUID
from .enums import BetStatus

class BetCreate(BaseModel):
    event_id: str
    amount: float = Field(..., gt=0)

class BetResponse(BaseModel):
    id: UUID
    event_id: str
    amount: float
    status: BetStatus
