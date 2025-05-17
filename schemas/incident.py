from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class IncidentCreate(BaseModel):
    title: str
    description: Optional[str] = None
    service_id: int
    organization_id: int

class IncidentUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    resolved_at: Optional[datetime]
    