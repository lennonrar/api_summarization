from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi_restful.cbv import cbv
from fastapi import status as http_status
from urllib.parse import unquote, urlparse

from app.dto.summary.create_summary_request import CreateSummaryRequest
from app.dto.summary.create_summary_response import CreateSummaryResponse
from app.dto.summary.get_summary_response import GetSummaryResponse
from app.services.container import get_summary_service
from app.services.summary.summary import SummaryService

router = APIRouter(prefix="/summary", tags=["summary"])

def validate_url_input(url2search: str = Query(..., description="URL to get summary for")) -> str:
    """Normalize and validate that URL is from Wikipedia"""
    # Decode if already encoded
    decoded_url = unquote(url2search)

    # Parse URL
    parsed = urlparse(decoded_url)

    # Validate Wikipedia domain
    domain = parsed.netloc.lower()
    if not (domain.endswith('.wikipedia.org') or domain == 'wikipedia.org'):
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail=f"Only Wikipedia URLs are allowed. Got domain: {domain}"
        )

    return decoded_url


@cbv(router)
class View:
    @router.get("/", status_code=http_status.HTTP_200_OK,)
    async def get_summary_by_url(
        self,
        url2search: str = Depends(validate_url_input),
        service: SummaryService = Depends(get_summary_service)
    ) -> GetSummaryResponse:
        summary_service_data = await service.get_summary_by_url(url2search)
        if not  summary_service_data:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="Summary not found for the provided URL."
            )

        return GetSummaryResponse(
            summary=summary_service_data.summary,
            url=summary_service_data.url
        )

    @router.post("/", status_code=http_status.HTTP_201_CREATED,)
    async def create_summary(
            self,
            summary_payload: CreateSummaryRequest,
            service: SummaryService = Depends(get_summary_service)
    ) -> CreateSummaryResponse:
        summary_service_data = await service.create_summary(
            url=str(summary_payload.url),
            words_limit=summary_payload.words_limit
        )
        return CreateSummaryResponse(summary=summary_service_data.summary, url=summary_service_data.url)

