from bs4 import BeautifulSoup as bs, BeautifulSoup

from app.shared.requests.requests import RequestService


class ScrapService:

    def __init__(self, request_service: RequestService):
        self.request_service = request_service

    async def scrap_data(self, url: str) -> BeautifulSoup:
        """Scrape text content from any web page.

        This is a generic scraper that removes common non-content elements
        and extracts the main text from the page.
        """
        html = await self.request_service.get_data(url, json_response=False)
        soup = bs(html, 'html.parser')

        # Remove unwanted elements (scripts, styles, navigation, etc.)
        for tag in soup(['script', 'style', 'nav', 'footer', 'header', 'aside', 'form']):
            tag.decompose()

        return soup