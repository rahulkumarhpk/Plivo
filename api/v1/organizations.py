from fastapi import APIRouter, Request, Depends, status, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from db.models import Organization
from core.decorators import validate_payload
from schemas.organization import OrganizationCreate, OrganizationUpdate

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
# @jwt_required
@validate_payload(OrganizationCreate)
async def create_organization(request: Request, validated_data: OrganizationCreate, db: Session = Depends(get_db)):
    org = Organization(name=validated_data.name)
    db.add(org)
    db.commit()
    db.refresh(org)
    return org

@router.get("/{org_id}")
# @jwt_required
async def get_organization(org_id: int, request: Request, db: Session = Depends(get_db)):
    org = db.query(Organization).filter(Organization.id == org_id).first()
    if not org:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
    return org

@router.put("/{org_id}")
# @jwt_required
@validate_payload(OrganizationUpdate)
async def update_organization(org_id: int, request: Request, validated_data: OrganizationUpdate, db: Session = Depends(get_db)):
    org = db.query(Organization).filter(Organization.id == org_id).first()
    if not org:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
    org.name = validated_data.name
    db.commit()
    db.refresh(org)
    return org

@router.delete("/{org_id}", status_code=status.HTTP_204_NO_CONTENT)
# @jwt_required
async def delete_organization(org_id: int, request: Request, db: Session = Depends(get_db)):
    org = db.query(Organization).filter(Organization.id == org_id).first()
    if not org:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
    db.delete(org)
    db.commit()
    return {"detail": "Organization deleted"}
