from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import docker

import crud, models, schemas
from database import SessionLocal, engine, get_db
from initial_data import init_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

try:
    print("Attempting to initialize the database...")
    init_db()
    print("Database initialization finished.")
except Exception as e:
    print(f"Error during database initialization: {e}")


client = docker.DockerClient(base_url='tcp://docker-proxy:2375')

@app.get("/api/resources", response_model=list[schemas.Resource])
def read_resources(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    resources = crud.get_resources(db, skip=skip, limit=limit)

    # Add status from docker
    for resource in resources:
        try:
            container = client.containers.get(resource.name.lower().replace(" ", "-"))
            resource.status = container.status
        except docker.errors.NotFound:
            resource.status = "Not Found"

    return resources

@app.post("/api/resources", response_model=schemas.Resource)
def create_resource(resource: schemas.ResourceCreate, db: Session = Depends(get_db)):
    return crud.create_resource(db=db, resource=resource)

@app.post("/api/resources/{resource_id}/start")
def start_resource(resource_id: int, db: Session = Depends(get_db)):
    db_resource = crud.get_resource(db, resource_id=resource_id)
    if db_resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")

    container_name = db_resource.name.lower().replace(" ", "-")

    try:
        container = client.containers.get(container_name)
        container.start()
        return {"message": f"{db_resource.name} started successfully"}
    except docker.errors.NotFound:
        try:
            client.containers.run(
                db_resource.docker_image_name,
                name=container_name,
                ports={f'{db_resource.internal_port}/tcp': db_resource.host_port},
                detach=True,
            )
            return {"message": f"{db_resource.name} created and started successfully"}
        except docker.errors.ImageNotFound:
            raise HTTPException(status_code=404, detail=f"Image {db_resource.docker_image_name} not found. Please pull the image first.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/resources/{resource_id}/stop")
def stop_resource(resource_id: int, db: Session = Depends(get_db)):
    db_resource = crud.get_resource(db, resource_id=resource_id)
    if db_resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")

    container_name = db_resource.name.lower().replace(" ", "-")

    try:
        container = client.containers.get(container_name)
        container.stop()
        return {"message": f"{db_resource.name} stopped successfully"}
    except docker.errors.NotFound:
        raise HTTPException(status_code=404, detail=f"Container for {db_resource.name} not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/resources/{resource_id}/pull")
def pull_resource(resource_id: int, db: Session = Depends(get_db)):
    db_resource = crud.get_resource(db, resource_id=resource_id)
    if db_resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")

    try:
        client.images.pull(db_resource.docker_image_name)
        return {"message": f"Image {db_resource.docker_image_name} pulled successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/resources/{resource_id}/update")
def update_resource(resource_id: int, db: Session = Depends(get_db)):
    db_resource = crud.get_resource(db, resource_id=resource_id)
    if db_resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")

    container_name = db_resource.name.lower().replace(" ", "-")

    try:
        # Stop and remove existing container
        try:
            container = client.containers.get(container_name)
            container.stop()
            container.remove()
        except docker.errors.NotFound:
            pass

        # Pull the latest image
        client.images.pull(db_resource.docker_image_name)

        # Start a new container
        client.containers.run(
            db_resource.docker_image_name,
            name=container_name,
            ports={f'{db_resource.internal_port}/tcp': db_resource.host_port},
            detach=True,
        )
        return {"message": f"{db_resource.name} updated and started successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
