import hashlib

from app.services.scrap.scrap_service import ScrapService
from app.services.summary.summary_repository import SummaryRepositoryInterface

class SummaryService:
    def __init__(
            self,
            summary_repository:  SummaryRepositoryInterface,
            scrap_service: ScrapService,
    ):
        self.summary_repository = summary_repository
        self.scrap_service = scrap_service

    async def get_summary_by_url(self, url: str) -> dict:
        # TODO
        ## Manipulação de API externa: A API precisaria acessar a página do Wikipedia,
        ## extrair o conteúdo, e resumir o texto.
        summary_id = hashlib.sha256(url.encode()).hexdigest()[:16]
        summary_data = self.summary_repository.get_summary_by_id(summary_id)
        ## consultar e reutilizar os resumos já gerados.
        return summary_data

    async def create_summary(self, url: str, words_limit: int) -> dict:
        html_content = await self.scrap_service.scrap_data(url)
        # TODO get id
        summary_id = hashlib.sha256(url.encode()).hexdigest()[:16]
        # TODO get summary from LLM
        summary = "This is a summary."
        summary_data = await self.get_summary_by_url(url);
        if summary_data['summary']:
            return summary_data['summary']

        return self.summary_repository.create_summary(summary_id, url, summary)


