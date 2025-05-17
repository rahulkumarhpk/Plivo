from fastapi import APIRouter, Request, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.session import get_db
from db.models import Incident
from schemas.incident import IncidentCreate, IncidentUpdate
from core.decorators import validate_payload

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
# @jwt_required
@validate_payload(IncidentCreate)
async def create_incident(request: Request, validated_data: IncidentCreate, db: Session = Depends(get_db)):
    incident = Incident(
        title=validated_data.title,
        description=validated_data.description,
        service_id=validated_data.service_id,
        organization_id=validated_data.organization_id
    )
    db.add(incident)
    db.commit()
    db.refresh(incident)
    return incident

import logging

# Set up logging at the top of the file
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.get("/{incident_id}")
# @jwt_required
async def get_incident(
    request: Request,  # FastAPI request object should typically come first
    incident_id: int,  # Path parameter
    db: Session = Depends(get_db),  # Database dependency
    # user: dict = Depends(get_current_user)  # Uncomment if using JWT
):
    logger.debug(f"Request headers: {dict(request.headers)}")
    logger.info(f"GET /incidents/{incident_id} called")
    try:
        incident = db.query(Incident).filter(Incident.id == incident_id).first()
        logger.info(f"Found incident: {incident}")
        if not incident:
            logger.warning(f"Incident with ID {incident_id} not found")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found")
        return incident
    except Exception as e:
        logger.error(f"Error in get_incident: {str(e)}")
        raise

@router.put("/{incident_id}")
# @jwt_required
@validate_payload(IncidentUpdate)
async def update_incident(incident_id: int, request: Request, validated_data: IncidentUpdate, db: Session = Depends(get_db)):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found")
    
    for attr, value in validated_data.dict(exclude_unset=True).items():
        setattr(incident, attr, value)

    db.commit()
    db.refresh(incident)
    return incident

@router.delete("/{incident_id}", status_code=status.HTTP_204_NO_CONTENT)
# @jwt_required
async def delete_incident(incident_id: int, request: Request, db: Session = Depends(get_db)):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found")
    
    db.delete(incident)
    db.commit()
    return {"detail": "Incident deleted"}
