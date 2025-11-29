from abc import ABC, abstractmethod
from sqlalchemy.orm import Session

from app.models.summary import Summary


class SummaryRepositoryInterface(ABC):
    @abstractmethod
    def get_summary_by_id(self, summary_id: str) -> dict | None:
        pass

    @abstractmethod
    def create_summary(self, summary_id: str, url: str, summary: str) -> dict:
        pass

class SummaryRepository(SummaryRepositoryInterface):
    """Repository to manage Summary data in the database."""
    def __init__(self, db: Session):
        self.db = db

    def get_summary_by_id(self, summary_id: str) -> dict | None:
        """Retrieve a summary by its ID."""
        result = self.db.query(Summary).filter(Summary.id == summary_id).first()
        return result


    def create_summary(self, summary_id: str, url: str, summary: str) -> dict:
        """Create a new summary record."""
        db_summary = Summary(id=summary_id, url=url, summary=summary)
        self.db.add(db_summary)
        self.db.commit()
        self.db.refresh(db_summary)
        return db_summary