from app.extensions import db
from datetime import datetime

class Incident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(50))  # investigating, identified, monitoring, resolved
    impact = db.Column(db.String(50))  # none, minor, major, critical
    type = db.Column(db.String(50))  # incident, maintenance
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    resolved_at = db.Column(db.DateTime)
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'))
    
    # Relationships
    updates = db.relationship('IncidentUpdate', backref='incident')
    affected_services = db.relationship('Service', secondary='incident_services')

class IncidentUpdate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    incident_id = db.Column(db.Integer, db.ForeignKey('incident.id'))
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
