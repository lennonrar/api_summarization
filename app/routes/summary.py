from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi_restful.cbv import cbv
from fastapi import status as http_status
from urllib.parse import unquote, urlparse

from app.dto.summary.create_summary_request import CreateSummaryRequest
from app.dto.summary.create_summary_response import CreateSummaryResponse
from app.dto.summary.get_summary_response import GetSummaryResponse

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
    async def get_summary_by_url(self, url2search: str = Depends(validate_url_input)) -> GetSummaryResponse:

        return GetSummaryResponse(summary=f"Summary from {url2search}")

    @router.post("/", status_code=http_status.HTTP_201_CREATED,)
    async def create_summary(self, summary_payload: CreateSummaryRequest) -> CreateSummaryResponse:
        return CreateSummaryResponse(summary=f"Created summary for {summary_payload.url}")

