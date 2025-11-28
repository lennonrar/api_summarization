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
        html_content = await self.scrap_service.scrap_data(url)
        ## Sumarização (LLM): Resumir o conteúdo da página usando uma técnica como
        ## sumarização utilizando a OpenAI
        summary = "Summary of the page"
        ## Banco de dados: Armazenar o resumo da página e criar endpoints para
        ## consultar e reutilizar os resumos já gerados.
        return self.summary_repository.get_summary_by_url(url)

    async def create_summary(self, user_id: int, url: str, summary: str) -> dict:
        return self.summary_repository.create_summary(user_id, url, summary)


