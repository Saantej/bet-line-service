from fastapi import APIRouter, HTTPException, Depends
from typing import List
from datetime import datetime
from .services import EventService
from .schemas import Event, UpdateEventResponse, EventResponse, EventCreateRequest
from .enums import EventStatus

router = APIRouter()

event_service = EventService()

@router.post("/events", response_model=EventResponse, summary="Create an event")
async def create_event(event: EventCreateRequest):
    """
    Create a new event for betting
    """
    if event.odds <= 0:
        raise HTTPException(status_code=400, detail="Odds must be a positive number")
    created_event = await event_service.create_event(event.odds, event.deadline)
    return created_event
   
@router.get("/events", response_model=List[Event], summary="Retrieve available events")
async def list_events():
    """
    Retrieve a list of events available for betting
    """
    return await event_service.get_available_events()

@router.patch("/events/{event_id}", response_model=UpdateEventResponse, summary="Update event status")
async def update_event_status(event_id: str, status: EventStatus):
    """
    Update the status of an event
    """
    updated_event = await event_service.update_event_status(event_id, status)
    if not updated_event:
        raise HTTPException(status_code=404, detail="Event not found")


    match status:
        case EventStatus.PENDING:
            message = "The event is still pending"
        case EventStatus.TEAM1_WIN:
            message = "The event was won by team 1"
        case EventStatus.TEAM1_LOSS:
            message = "The event was lost by team 1"
        case _:
            raise HTTPException(status_code=400, detail=f"Invalid status: {status}")

    updated_event.status = status
    return {
        "event": updated_event,
        "message": message
    }
