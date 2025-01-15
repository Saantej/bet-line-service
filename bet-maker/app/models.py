from sqlalchemy import Column, String, Float, Enum
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db import Base
from app.enums import BetStatus

class Bet(Base):
    __tablename__ = "bets"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(Enum(BetStatus), nullable=False, default=BetStatus.PENDING)
