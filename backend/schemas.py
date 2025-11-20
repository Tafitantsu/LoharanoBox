from pydantic import BaseModel
import datetime

class ResourceBase(BaseModel):
    name: str
    docker_image_name: str
    internal_port: int
    host_port: int
    description: str
    domain: str

class ResourceCreate(ResourceBase):
    pass

class Resource(ResourceBase):
    id: int
    is_active: bool
    last_consulted_date: datetime.datetime
    status: str = "Not Found"

    class Config:
        orm_mode = True
