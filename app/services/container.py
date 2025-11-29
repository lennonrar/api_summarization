from fastapi import Depends
from requests import Session

from app.services.language_models.language_models import LanguageModelsService
from app.services.scrap.scrap_service import ScrapService
from app.services.summary.summary import SummaryService
from app.services.summary.summary_repository import SummaryRepository
from app.shared.databases.connection import get_db
from app.shared.requests.requests import RequestService


def get_request_service() -> RequestService:
    return RequestService()

def get_scrap_service(request_service: RequestService = Depends(get_request_service)) -> ScrapService:
    return ScrapService(request_service)

def get_summary_repository(db: Session = Depends(get_db)) -> SummaryRepository:
    return SummaryRepository(db)

def get_language_models_service() -> LanguageModelsService:
    return LanguageModelsService()

def get_summary_service(
    summary_repository: SummaryRepository = Depends(get_summary_repository),
    scrap_service: ScrapService = Depends(get_scrap_service),
    language_models_service: LanguageModelsService = Depends(get_language_models_service)
) -> SummaryService:
    return SummaryService(summary_repository, scrap_service, language_models_service)