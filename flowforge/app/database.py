"""Database setup and session lifecycle management."""
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from flowforge.app.config import settings


class Base(DeclarativeBase):
    """Base class for ORM models."""


engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """Yield a database session for request-scoped dependencies."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
