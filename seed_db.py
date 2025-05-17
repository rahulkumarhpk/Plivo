from db.session import engine, Base, SessionLocal
from db.models import Organization, Team, Service, Incident, ServiceStatus
from datetime import datetime, timedelta, UTC
import random

def seed_database():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Create organizations (10 organizations)
        print("Creating organizations...")
        organizations = []
        org_names = [
            "Tech Corp", "Cloud Systems", "Digital Solutions", 
            "Network Inc", "Data Corp", "Security Solutions",
            "Web Services", "Platform Co", "DevOps Inc", "Infrastructure Ltd"
        ]
        
        for name in org_names:
            org = Organization(name=name)
            organizations.append(org)
        db.add_all(organizations)
        db.flush()

        # Create teams (3-5 teams per organization)
        print("Creating teams...")
        teams = []
        team_names = [
            "Platform", "Infrastructure", "Security", "DevOps", 
            "Database", "Frontend", "Backend", "QA", "SRE", "Network"
        ]
        
        for org in organizations:
            num_teams = random.randint(3, 5)
            selected_teams = random.sample(team_names, num_teams)
            for team_name in selected_teams:
                team = Team(
                    name=f"{team_name} Team",
                    organization_id=org.id
                )
                teams.append(team)
        db.add_all(teams)
        db.flush()

        # Create services (5-7 services per organization)
        print("Creating services...")
        services = []
        service_templates = [
            ("API Gateway", "Main API Gateway Service"),
            ("Authentication", "User Authentication System"),
            ("Database", "Main Database Cluster"),
            ("Storage", "Object Storage Service"),
            ("Cache", "Redis Cache Layer"),
            ("Search", "Elasticsearch Service"),
            ("Messaging", "Message Queue Service"),
            ("CDN", "Content Delivery Network"),
            ("Monitoring", "System Monitoring"),
            ("Logging", "Log Aggregation Service")
        ]
        
        for org in organizations:
            num_services = random.randint(5, 7)
            selected_services = random.sample(service_templates, num_services)
            for svc_name, svc_desc in selected_services:
                status = random.choice(list(ServiceStatus))
                service = Service(
                    name=f"{svc_name}",
                    status=status,
                    description=svc_desc,
                    organization_id=org.id
                )
                services.append(service)
        db.add_all(services)
        db.flush()

        # Create incidents (2-4 incidents per service)
        print("Creating incidents...")
        incidents = []
        incident_types = ["incident", "maintenance"]
        impact_levels = ["minor", "major", "critical"]
        status_types = ["investigating", "identified", "monitoring", "resolved"]
        
        incident_templates = [
            "Increased latency in {}",
            "{} performance degradation",
            "{} connectivity issues",
            "Scheduled maintenance for {}",
            "{} system upgrade",
            "{} security patch deployment",
            "Unexpected {} outage",
            "{} capacity issues"
        ]
        
        for service in services:
            num_incidents = random.randint(2, 4)
            for _ in range(num_incidents):
                started_at = datetime.now(UTC) - timedelta(days=random.randint(1, 30))
                resolved = random.choice([True, False])
                
                incident = Incident(
                    title=random.choice(incident_templates).format(service.name),
                    description=f"Issue affecting {service.name} service",
                    # Field names should match the model definition:
                    created_at=started_at,
                    resolved_at=started_at + timedelta(hours=random.randint(1, 24)) if resolved else None,
                    service_id=service.id,
                    organization_id=service.organization_id
                )
                incidents.append(incident)
        
        db.add_all(incidents)
        db.commit()
        
        print(f"""Database seeded successfully!
        Created:
        - {len(organizations)} organizations
        - {len(teams)} teams
        - {len(services)} services
        - {len(incidents)} incidents""")

    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()