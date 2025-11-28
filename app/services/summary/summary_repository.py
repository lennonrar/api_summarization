from abc import ABC, abstractmethod

class SummaryRepositoryInterface(ABC):
    @abstractmethod
    def get_summary_by_url(self, url: int) -> dict:
        pass

    @abstractmethod
    def create_summary(self, user_id: int, url: str, summary: str) -> dict:
        pass