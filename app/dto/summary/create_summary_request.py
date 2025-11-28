from urllib.parse import urlparse
from pydantic import BaseModel, HttpUrl, field_validator


class CreateSummaryRequest(BaseModel):
    url: HttpUrl
    words: int

    @field_validator('url')
    @classmethod
    def validate_wikipedia_url(cls, v: HttpUrl) -> HttpUrl:
        """Validate that URL is from Wikipedia"""
        # Convert HttpUrl to string for parsing
        url_str = str(v)
        parsed = urlparse(url_str)

        # Validate Wikipedia domain
        domain = parsed.netloc.lower()
        if not (domain.endswith('.wikipedia.org') or domain == 'wikipedia.org'):
            raise ValueError(f"Only Wikipedia URLs are allowed")

        return v

