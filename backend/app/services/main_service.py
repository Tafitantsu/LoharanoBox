from app.db.init_db import init_db
from app.db.session import SessionLocal

def onstart():
    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close()