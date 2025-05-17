from fastapi import APIRouter, Request, Depends, status, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from db.models import Service
from core.decorators import validate_payload
from schemas.service import ServiceCreate, ServiceUpdate

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
# @jwt_required
@validate_payload(ServiceCreate)
async def create_service(request: Request, validated_data: ServiceCreate, db: Session = Depends(get_db)):
    service = Service(
        name=validated_data.name,
        status=validated_data.status,
        description=validated_data.description,
        organization_id=validated_data.organization_id,
    )
    db.add(service)
    db.commit()
    db.refresh(service)
    return service

@router.get("/{service_id}")
# @jwt_required
async def get_service(service_id: int, request: Request, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
    return service

@router.put("/{service_id}")
# @jwt_required
@validate_payload(ServiceUpdate)
async def update_service(service_id: int, request: Request, validated_data: ServiceUpdate, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
    
    update_data = validated_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(service, key, value)
    
    db.commit()
    db.refresh(service)
    return service

@router.delete("/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
# @jwt_required
async def delete_service(service_id: int, request: Request, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
    db.delete(service)
    db.commit()
    return {"detail": "Service deleted"}
