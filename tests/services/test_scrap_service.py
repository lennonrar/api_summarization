"""
Tests for ScrapService
"""
import pytest
from unittest.mock import Mock, AsyncMock
from bs4 import BeautifulSoup

from app.services.scrap.scrap_service import ScrapService
from app.shared.requests.requests import RequestService


class TestScrapService:
    """Test the ScrapService"""

    @pytest.fixture
    def mock_request_service(self):
        """Create mock request service"""
        service = Mock(spec=RequestService)
        service.get_data = AsyncMock()
        return service

    @pytest.fixture
    def scrap_service(self, mock_request_service):
        """Create ScrapService with mocked dependencies"""
        return ScrapService(request_service=mock_request_service)

    @pytest.mark.asyncio
    async def test_scrap_data_success(self, scrap_service, mock_request_service):
        """Test scraping data from URL - SUCCESS case"""
        # Arrange
        test_url = "https://en.wikipedia.org/wiki/Python"
        html_content = b"""
        <html>
            <head><title>Python</title></head>
            <body>
                <nav>Navigation</nav>
                <div id="content">
                    <p>Python is a programming language.</p>
                    <p>It was created by Guido van Rossum.</p>
                </div>
                <script>console.log('test');</script>
                <footer>Footer content</footer>
            </body>
        </html>
        """
        mock_request_service.get_data.return_value = html_content

        # Act
        result = await scrap_service.scrap_data(test_url)

        # Assert
        assert isinstance(result, BeautifulSoup)
        # Check that unwanted elements are removed
        assert result.find('script') is None
        assert result.find('nav') is None
        assert result.find('footer') is None
        # Check that content is preserved
        assert result.find('p') is not None
        text = result.get_text()
        assert "Python is a programming language" in text
        mock_request_service.get_data.assert_called_once_with(test_url, json_response=False)
