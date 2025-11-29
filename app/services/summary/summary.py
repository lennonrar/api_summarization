import hashlib

from app.services.scrap.scrap_service import ScrapService
from app.services.summary.summary_repository import SummaryRepositoryInterface
from app.services.language_models.language_models import LanguageModelsService



class SummaryService:
    """Service to manage summaries for URLs."""
    def __init__(
            self,
            summary_repository:  SummaryRepositoryInterface,
            scrap_service: ScrapService,
            language_models_service: LanguageModelsService,
    ):
        self.summary_repository = summary_repository
        self.scrap_service = scrap_service
        self.language_models_service = language_models_service

    def _generate_summary_id(self, url: str) -> str:
        """Generate a unique ID from URL"""
        return hashlib.sha256(url.encode()).hexdigest()[:16]

    async def get_summary_by_url(self, url: str) -> dict:
        """Get summary for the given URL"""
        summary_id = self._generate_summary_id(url)
        summary_data = self.summary_repository.get_summary_by_id(summary_id)

        return summary_data

    async def create_summary(self, url: str, words_limit: int) -> dict:
        """Create summary for the given URL"""
        summary_id = self._generate_summary_id(url)

        # Check if summary already exists
        summary_data = await self.get_summary_by_url(url)
        if summary_data and summary_data.summary:
            return summary_data

        # Scrape content and generate summary
        soup_content = await self.scrap_service.scrap_data(url)
        content = soup_content.find('div', {'id': 'mw-content-text'})
        text_content = soup_content.get_text()
        if content:
            paragraphs = content.find_all('p')
            text_content = '\n'.join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])

        summary = await self.language_models_service.generate_summary(text_content, words_limit)

        return self.summary_repository.create_summary(summary_id, url, summary)
