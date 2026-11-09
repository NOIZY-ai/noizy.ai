"""
🗄️ DATABASE CONNECTION - 100% PERFECT
Perfect database connection management
GORUNFREE Protocol
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from typing import Generator
from ..config import settings
from ..logging import get_logger

logger = get_logger("database")

# Create engine with connection pooling
engine = create_engine(
    settings.DATABASE_URL,
    poolclass=QueuePool,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    pool_pre_ping=True,  # Verify connections before using
    echo=False
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    Get database session (dependency)
    
    Yields:
        Database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Initialize database (create tables)"""
    from .schema import Base
    Base.metadata.create_all(bind=engine)
    logger.info("database_initialized")


def check_db_connection() -> bool:
    """
    Check database connection
    
    Returns:
        True if connected, False otherwise
    """
    try:
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        return True
    except Exception as e:
        logger.error("database_connection_failed", error=str(e))
        return False

