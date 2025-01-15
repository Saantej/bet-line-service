import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import Bet
from .schemas import BetCreate
from .enums import BetStatus
from fastapi import HTTPException
from typing import List, Dict, Any

class BetService:
    def __init__(self):
        """
        Initialize the HTTP client for the event provider
        """
        self.client = httpx.AsyncClient(base_url="http://line-provider:8000")

    async def get_available_events(self) -> List[Dict[str, Any]]:
        """
        Fetch the list of available events
        """
        try:
            response = await self.client.get("/events")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=500, detail=f"Error fetching events: {str(e)}")
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Request failed: {str(e)}")

    def create_bet_object(self, bet: BetCreate) -> Bet:
        """
        Create a Bet object from input data
        """
        return Bet(event_id=bet.event_id, amount=bet.amount, status=BetStatus.PENDING)

    async def create_bet(self, bet: BetCreate, db: AsyncSession) -> Bet:
        """
        Validate event ID and create a new bet
        """
        events = await self.get_available_events()
        event_dict = {event["id"]: event for event in events}
        if bet.event_id not in event_dict:
            raise HTTPException(status_code=400, detail="Event not found")
        
        new_bet = self.create_bet_object(bet)
        db.add(new_bet)
        await db.commit()
        await db.refresh(new_bet)
        return new_bet

    async def get_bets(self, db: AsyncSession) -> List[Bet]:
        """
        Retrieve all bets from the database
        """
        result = await db.execute(select(Bet))
        return result.scalars().all()
