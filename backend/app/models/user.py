import uuid
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Table, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.db.base_class import Base

# Association table for roles and permissions
role_permission_association = Table(
    'role_permission', Base.metadata,
    Column('role_id', UUID(as_uuid=True), ForeignKey('roles.id'), primary_key=True),
    Column('permission_id', UUID(as_uuid=True), ForeignKey('permissions.id'), primary_key=True)
)

class Role(Base):
    __tablename__ = 'roles'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nom = Column(String, unique=True, nullable=False)
    permissions = relationship("Permission", secondary=role_permission_association, back_populates="roles")

class Permission(Base):
    __tablename__ = 'permissions'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nom = Column(String, unique=True, nullable=False)
    roles = relationship("Role", secondary=role_permission_association, back_populates="permissions")

class User(Base):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False, index=True)
    mot_de_passe = Column(String, nullable=False)
    actif = Column(Boolean, default=True)
    date_creation = Column(DateTime, server_default=func.now())
    role_id = Column(UUID(as_uuid=True), ForeignKey('roles.id'))
    role = relationship("Role")
    suggestions = relationship("Suggestion", back_populates="utilisateur")
