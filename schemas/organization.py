from pydantic import BaseModel

class OrganizationCreate(BaseModel):
    name: str

class OrganizationUpdate(BaseModel):
    name: str
