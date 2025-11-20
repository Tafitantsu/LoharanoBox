from sqlalchemy.orm import Session
import crud, schemas
from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

def init_db():
    db = SessionLocal()
    print("Initializing database...")
    if db.query(models.Resource).count() > 0:
        print("Database already initialized.")
        db.close()
        return

    resources = [
        # Development
        schemas.ResourceCreate(
            name="DevDocs Offline",
            docker_image_name="montyfi/devdocs",
            internal_port=80,
            host_port=8080,
            description="API documentation for various technologies.",
            domain="Development",
        ),
        schemas.ResourceCreate(
            name="W3Schools Offline",
            docker_image_name="ja7adr/w3schools",
            internal_port=80,
            host_port=8081,
            description="Web tutorials.",
            domain="Development",
        ),
        schemas.ResourceCreate(
            name="Python Docs",
            docker_image_name="python:3.9-docs",
            internal_port=80,
            host_port=8082,
            description="Python documentation.",
            domain="Development",
        ),
        # DevOps
        schemas.ResourceCreate(
            name="Gitea Server",
            docker_image_name="gitea/gitea:latest",
            internal_port=3000,
            host_port=3000,
            description="Lightweight Git server.",
            domain="DevOps",
        ),
        schemas.ResourceCreate(
            name="Prometheus",
            docker_image_name="prom/prometheus",
            internal_port=9090,
            host_port=9090,
            description="Monitoring system.",
            domain="DevOps",
        ),
        schemas.ResourceCreate(
            name="Grafana",
            docker_image_name="grafana/grafana",
            internal_port=3000,
            host_port=3001,
            description="Metrics visualization.",
            domain="DevOps",
        ),
        # Cybersecurity
        schemas.ResourceCreate(
            name="OWASP Juice Shop",
            docker_image_name="bkimminich/juice-shop",
            internal_port=3000,
            host_port=4000,
            description="Web application security training.",
            domain="Cybersecurity",
        ),
        schemas.ResourceCreate(
            name="DVWA",
            docker_image_name="vulnerables/web-dvwa",
            internal_port=80,
            host_port=4001,
            description="Damn Vulnerable Web Application.",
            domain="Cybersecurity",
        ),
    ]

    for resource in resources:
        crud.create_resource(db=db, resource=resource)

    print("Database initialized successfully.")
    db.close()
