from sqlalchemy import Column, Integer, String, Boolean, DateTime
from database import Base
import datetime

class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    docker_image_name = Column(String)
    internal_port = Column(Integer)
    host_port = Column(Integer)
    description = Column(String)
    domain = Column(String)
    is_active = Column(Boolean, default=True)
    last_consulted_date = Column(DateTime, default=datetime.datetime.utcnow)
