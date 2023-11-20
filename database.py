# database.py
from sqlalchemy.orm import sessionmaker, Session

# Use scoped_session to create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False)

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
