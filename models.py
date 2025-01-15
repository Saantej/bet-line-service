from pydantic import BaseModel

class Event(BaseModel):
    id: str
    coefficient: float
    deadline: int
    status: str
    