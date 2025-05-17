from pydantic import BaseModel
from typing import Optional
from db.models import ServiceStatus

class ServiceCreate(BaseModel):
    name: str
    status: ServiceStatus = ServiceStatus.OPERATIONAL
    description: Optional[str] = None
    organization_id: int

class ServiceUpdate(BaseModel):
    name: Optional[str]
    status: Optional[ServiceStatus]
    description: Optional[str]
