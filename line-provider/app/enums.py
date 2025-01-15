from enum import Enum

class EventStatus(str, Enum):
    PENDING = "pending"       
    TEAM1_WIN = "team1_win"   
    TEAM1_LOSS = "team1_loss"  
