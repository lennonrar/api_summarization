"""
Tests for SummaryService
"""
import pytest
from unittest.mock import Mock, AsyncMock, MagicMock
from bs4 import BeautifulSoup

from app.services.summary.summary import SummaryService
from app.services.summary.summary_repository import SummaryRepositoryInterface
from app.services.scrap.scrap_service import ScrapService
from app.services.language_models.language_models import LanguageModelsService


class TestSummaryService:
    """Test the SummaryService"""

    @pytest.fixture
    def mock_repository(self):
        """Create mock repository"""
        repository = Mock(spec=SummaryRepositoryInterface)
        return repository

    @pytest.fixture
    def mock_scrap_service(self):
        """Create mock scrap service"""
        service = Mock(spec=ScrapService)
        service.scrap_data = AsyncMock()
        return service

    @pytest.fixture
    def mock_language_models_service(self):
        """Create mock language models service"""
        service = Mock(spec=LanguageModelsService)
        service.generate_summary = AsyncMock()
        return service

    @pytest.fixture
    def summary_service(self, mock_repository, mock_scrap_service, mock_language_models_service):
        """Create SummaryService with mocked dependencies"""
        return SummaryService(
            summary_repository=mock_repository,
            scrap_service=mock_scrap_service,
            language_models_service=mock_language_models_service
        )

    @pytest.mark.asyncio
    async def test_get_summary_by_url_success(self, summary_service, mock_repository):
        """Test getting existing summary by URL - SUCCESS case"""
        # Arrange
        test_url = "https://en.wikipedia.org/wiki/Python"
        mock_summary = MagicMock()
        mock_summary.id = "abc123def456"
        mock_summary.url = test_url
        mock_summary.summary = "Python is a high-level programming language."

        mock_repository.get_summary_by_id.return_value = mock_summary

        # Act
        result = await summary_service.get_summary_by_url(test_url)

        # Assert
        assert result is not None
        assert result.url == test_url
        assert result.summary == "Python is a high-level programming language."
        mock_repository.get_summary_by_id.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_summary_by_url_not_found(self, summary_service, mock_repository):
        """Test getting non-existing summary by URL - FAIL case"""
        # Arrange
        test_url = "https://en.wikipedia.org/wiki/NonExistentPage"
        mock_repository.get_summary_by_id.return_value = None

        # Act
        result = await summary_service.get_summary_by_url(test_url)

        # Assert
        assert result is None
        mock_repository.get_summary_by_id.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_summary_success(
        self,
        summary_service,
        mock_repository,
        mock_scrap_service,
        mock_language_models_service
    ):
        """Test creating new summary - SUCCESS case"""
        # Arrange
        test_url = "https://en.wikipedia.org/wiki/Machine_Learning"
        test_words_limit = 100

        # Mock no existing summary
        mock_repository.get_summary_by_id.return_value = None

        # Mock scraped content
        html_content = """
        <html>
            <div id="mw-content-text">
                <p>Machine learning is a subset of AI.</p>
                <p>It uses statistical techniques.</p>
            </div>
        </html>
        """
        mock_soup = BeautifulSoup(html_content, 'html.parser')
        mock_scrap_service.scrap_data.return_value = mock_soup

        # Mock LLM summary
        mock_language_models_service.generate_summary.return_value = "Machine learning summary."

        # Mock repository create
        mock_created_summary = MagicMock()
        mock_created_summary.url = test_url
        mock_created_summary.summary = "Machine learning summary."
        mock_repository.create_summary.return_value = mock_created_summary

        # Act
        result = await summary_service.create_summary(test_url, test_words_limit)

        # Assert
        assert result is not None
        assert result.summary == "Machine learning summary."
        mock_scrap_service.scrap_data.assert_called_once_with(test_url)
        mock_language_models_service.generate_summary.assert_called_once()
        mock_repository.create_summary.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_summary_returns_existing(
        self,
        summary_service,
        mock_repository,
        mock_scrap_service,
        mock_language_models_service
    ):
        """Test creating summary when it already exists - returns existing"""
        # Arrange
        test_url = "https://en.wikipedia.org/wiki/Existing_Page"
        test_words_limit = 100

        # Mock existing summary
        mock_existing_summary = MagicMock()
        mock_existing_summary.url = test_url
        mock_existing_summary.summary = "Existing summary."
        mock_repository.get_summary_by_id.return_value = mock_existing_summary

        # Act
        result = await summary_service.create_summary(test_url, test_words_limit)

        # Assert
        assert result == mock_existing_summary
        assert result.summary == "Existing summary."
        # Should not call scraping or LLM services
        mock_scrap_service.scrap_data.assert_not_called()
        mock_language_models_service.generate_summary.assert_not_called()
        mock_repository.create_summary.assert_not_called()

    def test_generate_summary_id(self, summary_service):
        """Test URL to ID generation is consistent"""
        # Arrange
        test_url = "https://en.wikipedia.org/wiki/Test"

        # Act
        id1 = summary_service._generate_summary_id(test_url)
        id2 = summary_service._generate_summary_id(test_url)

        # Assert
        assert id1 == id2
        assert len(id1) == 16  # SHA256 first 16 chars
        assert isinstance(id1, str)

