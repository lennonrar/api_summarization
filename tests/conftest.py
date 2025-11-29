"""
Test configuration and fixtures
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, AsyncMock
from app.main import app
from app.services.container import get_summary_service
from app.services.summary.summary import SummaryService


@pytest.fixture
def mock_summary_service():
    """Create a mock summary service for testing"""
    service = Mock(spec=SummaryService)
    service.get_summary_by_url = AsyncMock()
    service.create_summary = AsyncMock()
    return service


@pytest.fixture
def client(mock_summary_service):
    """Create a test client with mocked dependencies"""

    def override_get_summary_service():
        return mock_summary_service

    app.dependency_overrides[get_summary_service] = override_get_summary_service

    with TestClient(app) as test_client:
        yield test_client

    # Clean up
    app.dependency_overrides.clear()

