from pydantic import BaseModel, HttpUrl


class GetSummaryResponse(BaseModel):
    summary: str
