from bs4 import BeautifulSoup as bs

from app.shared.requests.requests import RequestService


class ScrapService:

    def __init__(self, request_service: RequestService):
        self.request_service = request_service

    async def scrap_data(self, url: str) -> dict:
        # Placeholder implementation for scraping data from a URL
        # In a real implementation, this would involve making HTTP requests
        # and parsing the response content.

        html_content: str = await self.request_service.get_requests(url, json_response=False)
        return bs(html_content, 'html.parser')

