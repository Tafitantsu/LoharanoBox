from sqlalchemy.engine import Engine
from app.db.base import Base

def init_db(engine: Engine):
    """
    Initialize the database by creating all tables.
    Optionally, insert seed data here.
    """
    Base.metadata.create_all(bind=engine)

    # Example seed data (uncomment and modify as needed)
    # from app.db.session import SessionLocal
    # from app.models.user import User
    # session = SessionLocal()
    # try:
    #     if not session.query(User).count():
    #         user = User(username="admin", email="admin@example.com", hashed_password="hashedpw")
    #         session.add(user)
    #         session.commit()
    # finally:
    #     session.close()
