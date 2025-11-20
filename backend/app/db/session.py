from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# SQLAlchemy engine
engine = create_engine(
    settings.DATABASE_URI,
    pool_pre_ping=True
)

# Session local class
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    """
    Dependency to get DB session. Yields a session and closes it after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
