"""
Tests for POST /summary endpoint
"""
from fastapi import status
from unittest.mock import MagicMock


class TestCreateSummaryRouter:
    """Test the POST /summary endpoint"""

    def test_create_summary_success(self, client, mock_summary_service):
        """Test creating summary for Wikipedia URL - SUCCESS case"""
        # Arrange
        test_url = "https://en.wikipedia.org/wiki/Artificial_intelligence"
        test_words_limit = 150
        mock_summary_data = MagicMock()
        mock_summary_data.summary = "Artificial intelligence (AI) is intelligence demonstrated by machines."
        mock_summary_data.url = test_url

        mock_summary_service.create_summary.return_value = mock_summary_data

        request_payload = {
            "url": test_url,
            "words_limit": test_words_limit
        }

        # Act
        response = client.post("/summary/", json=request_payload)

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        response_data = response.json()
        assert "summary" in response_data
        assert "url" in response_data
        assert response_data["summary"] == "Artificial intelligence (AI) is intelligence demonstrated by machines."
        assert response_data["url"] == test_url
        mock_summary_service.create_summary.assert_called_once_with(
            url=test_url,
            words_limit=test_words_limit
        )

    def test_create_summary_invalid_url_domain(self, client, mock_summary_service):
        """Test creating summary with non-Wikipedia URL - FAIL case"""
        # Arrange
        test_url = "https://github.com/some/repo"
        request_payload = {
            "url": test_url,
            "words_limit": 100
        }

        # Act
        response = client.post("/summary/", json=request_payload)

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        response_data = response.json()
        assert "detail" in response_data
        # Service should not be called for invalid URLs
        mock_summary_service.create_summary.assert_not_called()

    def test_create_summary_invalid_url_format(self, client, mock_summary_service):
        """Test creating summary with invalid URL format - FAIL case"""
        # Arrange
        request_payload = {
            "url": "not-a-valid-url",
            "words_limit": 100
        }

        # Act
        response = client.post("/summary/", json=request_payload)

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        response_data = response.json()
        assert "detail" in response_data
        mock_summary_service.create_summary.assert_not_called()

    def test_create_summary_missing_url(self, client, mock_summary_service):
        """Test creating summary without URL - FAIL case"""
        # Arrange
        request_payload = {
            "words_limit": 100
        }

        # Act
        response = client.post("/summary/", json=request_payload)

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        response_data = response.json()
        assert "detail" in response_data
        mock_summary_service.create_summary.assert_not_called()

    def test_create_summary_with_different_wikipedia_subdomain(self, client, mock_summary_service):
        """Test creating summary with different Wikipedia language subdomain - SUCCESS case"""
        # Arrange
        test_url = "https://fr.wikipedia.org/wiki/Intelligence_artificielle"
        mock_summary_data = MagicMock()
        mock_summary_data.summary = "L'intelligence artificielle est une discipline scientifique."
        mock_summary_data.url = test_url

        mock_summary_service.create_summary.return_value = mock_summary_data

        request_payload = {
            "url": test_url,
            "words_limit": 120
        }

        # Act
        response = client.post("/summary/", json=request_payload)

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        response_data = response.json()
        assert response_data["url"] == test_url
        mock_summary_service.create_summary.assert_called_once_with(
            url=test_url,
            words_limit=120
        )

    def test_create_summary_with_custom_words_limit(self, client, mock_summary_service):
        """Test creating summary with custom words_limit - SUCCESS case"""
        # Arrange
        test_url = "https://en.wikipedia.org/wiki/Deep_learning"
        test_words_limit = 250
        mock_summary_data = MagicMock()
        mock_summary_data.summary = "Deep learning is part of machine learning methods."
        mock_summary_data.url = test_url

        mock_summary_service.create_summary.return_value = mock_summary_data

        request_payload = {
            "url": test_url,
            "words_limit": test_words_limit
        }

        # Act
        response = client.post("/summary/", json=request_payload)

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        mock_summary_service.create_summary.assert_called_once_with(
            url=test_url,
            words_limit=test_words_limit
        )

    def test_create_summary_empty_request_body(self, client, mock_summary_service):
        """Test creating summary with empty request body - FAIL case"""
        # Act
        response = client.post("/summary/", json={})

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        mock_summary_service.create_summary.assert_not_called()

