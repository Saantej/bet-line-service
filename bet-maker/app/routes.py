from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .db import get_db
from app.schemas import BetCreate, BetResponse
from .services import BetService

router = APIRouter()
bet_service = BetService()

@router.get("/events", summary="Get available events")
async def get_events():
    """
    Fetch all available events for betting
    """
    return await bet_service.get_available_events()

@router.post("/bet", response_model=BetResponse, summary="Create a bet")
async def create_bet(bet: BetCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new bet for the given event
    """
    return await bet_service.create_bet(bet, db)

@router.get("/bets", response_model=List[BetResponse], summary="Get all bets")
async def get_bets(db: AsyncSession = Depends(get_db)):
    """
    Retrieve all bets from the database
    """
    return await bet_service.get_bets(db)
