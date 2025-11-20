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
    This function assumes that the database have already
    been created by running the Alembic migrations.
    """    

    # Check if the superuser already exists.
    try:
        admin_user = db.query(User).filter(User.email == settings.ADMIN_EMAIL).first()

        # If the superuser does not exist, create it.
        if not admin_user:
            hashed_password = get_password_hash(settings.ADMIN_PASSWORD)
            admin_user = User(
                email=settings.ADMIN_EMAIL,
                mot_de_passe=hashed_password,
                actif=True,
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            logger.info(f"Superuser {settings.ADMIN_EMAIL} created successfully.")
        else:
            logger.info(f"Superuser {settings.ADMIN_EMAIL} already exists. No action taken.")
    except ValueError:
        return "may be the database haven't already been created by running the Alembic migrations"