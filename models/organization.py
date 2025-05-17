from app.extensions import db
from datetime import datetime

class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    users = db.relationship('User', secondary='organization_users')
    services = db.relationship('Service', backref='organization')
    incidents = db.relationship('Incident', backref='organization')
