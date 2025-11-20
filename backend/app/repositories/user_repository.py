from sqlalchemy.orm import Session, joinedload
from app.models.user import User, Role
from app.schemas.user import UserCreate, UserUpdate
import uuid
from typing import List, Optional

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_users(self) -> List[User]:
        """
        Retrieves all users with their roles and permissions eagerly loaded.
        """
        return self.db.query(User).options(
            joinedload(User.role).joinedload(Role.permissions)
        ).order_by(User.email).all()

    def get_user_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        """
        Retrieves a single user by ID with their role and permissions eagerly loaded.
        """
        return self.db.query(User).options(
            joinedload(User.role).joinedload(Role.permissions)
        ).filter(User.id == user_id).first()

    def update_user(self, user_id: uuid.UUID, user_in: UserUpdate) -> Optional[User]:
        db_user = self.get_user_by_id(user_id)
        if db_user:
            update_data = user_in.model_dump(exclude_unset=True)
            if "mot_de_passe" in update_data:
                # This should be handled in the service layer to hash the password
                del update_data["mot_de_passe"]

            for key, value in update_data.items():
                setattr(db_user, key, value)

            self.db.commit()
            self.db.refresh(db_user)
        return db_user

    def create_user(self, user: UserCreate, hashed_password: str, role_id: uuid.UUID) -> User:
        db_user = User(
            email=user.email,
            mot_de_passe=hashed_password,
            role_id=role_id,
            actif=True  # Always active by default
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_user_by_email(self, email: str) -> User | None:
        """
        Retrieves a single user by email with their role and permissions eagerly loaded.
        This is crucial for authentication checks.
        """
        return self.db.query(User).options(
            joinedload(User.role).joinedload(Role.permissions)
        ).filter(User.email == email).first()

    def get_role_by_name(self, role_name: str) -> Role | None:
        return self.db.query(Role).filter(Role.nom == role_name).first()