from sqlalchemy.orm import Session
from app.core.config import settings
from app.db import base  # noqa: F401
from app.models.user import Role, User
from app.core.security import get_password_hash
import logging

# Configure logger
logger = logging.getLogger(__name__)

def init_db(db: Session) -> None:
    """
    Initializes the database by creating the superuser.
    This function assumes that the database roles and permissions have already
    been created by running the Alembic migrations.
    """
    # Attempt to find the admin role, which should have been created by migrations.
    admin_role = db.query(Role).filter(Role.nom == "admin").first()

    # If the admin role doesn't exist, it means migrations haven't been run.
    # This is a critical state, so we raise an error.
    if not admin_role:
        error_msg = (
            "The 'admin' role was not found in the database. "
            "This is likely because the Alembic migrations have not been run. "
            "Please run 'alembic upgrade head' to create the database schema and "
            "seed initial roles and permissions before starting the application."
        )
        logger.critical(error_msg)
        raise RuntimeError(error_msg)

    # Check if the superuser already exists.
    admin_user = db.query(User).filter(User.email == settings.ADMIN_EMAIL).first()

    # If the superuser does not exist, create it.
    if not admin_user:
        hashed_password = get_password_hash(settings.ADMIN_PASSWORD)
        admin_user = User(
            email=settings.ADMIN_EMAIL,
            mot_de_passe=hashed_password,
            actif=True,
            role_id=admin_role.id  # Assign the admin role ID.
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        logger.info(f"Superuser {settings.ADMIN_EMAIL} created successfully.")
    else:
        logger.info(f"Superuser {settings.ADMIN_EMAIL} already exists. No action taken.")