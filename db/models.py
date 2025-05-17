from sqlalchemy import Column, String, Integer, Enum, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from db.session import Base
import enum

class ServiceStatus(str, enum.Enum):
    OPERATIONAL = "Operational"
    DEGRADED = "Degraded Performance"
    PARTIAL_OUTAGE = "Partial Outage"
    MAJOR_OUTAGE = "Major Outage"

class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    teams = relationship("Team", back_populates="organization")
    services = relationship("Service", back_populates="organization")
    incidents = relationship("Incident", back_populates="organization")

class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    organization = relationship("Organization", back_populates="teams")

class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    status = Column(Enum(ServiceStatus), default=ServiceStatus.OPERATIONAL)
    description = Column(Text)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    organization = relationship("Organization", back_populates="services")
    incidents = relationship("Incident", back_populates="service")

class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)
    service_id = Column(Integer, ForeignKey("services.id"))
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    service = relationship("Service", back_populates="incidents")
    organization = relationship("Organization", back_populates="incidents")
