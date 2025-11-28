import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from app.db import Base

# Database configuration from environment variables
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://default:summarization_pass@localhost:5432/api_summarization"
)

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Enable connection health checks
    pool_size=5,  # Maximum number of connections to keep in the pool
    max_overflow=10,  # Maximum number of connections that can be created beyond pool_size
    echo=False,  # Set to True to log all SQL statements
)

# Create SessionLocal class for database sessions
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency function to get database session.
    Yields a database session and ensures it's closed after use.

    Usage in FastAPI:
        @app.get("/items")
        def read_items(db: Session = Depends(get_db)):
            # Use db here
            pass
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """
    Initialize database tables.
    This should be called on application startup.
    """
    pass
    # Base.metadata.create_all(bind=engine)

