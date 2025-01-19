from typing import List, Optional
from uuid import uuid4
from datetime import datetime, timezone
from .schemas import Event
from .enums import EventStatus

class EventService:
    def __init__(self):
        self.events = {}

    async def create_event(self, odds: float, deadline: datetime) -> Event:
        """
        Create a new event
        """
        event_id = str(uuid4())
        event = Event(
            id=event_id,
            odds=round(odds, 2),
            deadline=deadline,
            status=EventStatus.PENDING,  
        )
        self.events[event_id] = event
        return event
        
    async def get_available_events(self) -> List[Event]:
        now = datetime.now(timezone.utc)
        available_events = [
            event for event in self.events.values()
            if event.status == EventStatus.PENDING and event.deadline > now
        ]
        return available_events


    async def update_event_status(self, event_id: str, status: EventStatus) -> Optional[Event]:
        """
        Update the status of the event
        """
        event = self.events.get(event_id)
        if not event:
            return None
        event.status = status
        return event
