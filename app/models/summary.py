# models/summary.py
from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.sql import func

from app.db import Base


class Summary(Base):
    __tablename__ = "summaries"

    # Option 1: Hash as PK
    id = Column(String(64), primary_key=True)  # URL hash
    url = Column(String(2048), unique=True, nullable=False, index=True)
    summary = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
