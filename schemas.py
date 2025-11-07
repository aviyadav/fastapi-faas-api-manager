from typing import Optional
from pydantic import BaseModel

# Pydantic model for DynamicRoute
class RouteCreate(BaseModel):
    path: str
    message: Optional[str] = "Default Message"
    method: str = "GET"
    code: Optional[str] = None

class RouteResponse(RouteCreate):
    id: int

    class Config:
        orm_mode = True