"""
Tests for GET /summary endpoint
"""
from fastapi import status
from unittest.mock import MagicMock
from urllib.parse import quote


class TestGetSummaryRouter:
    """Test the GET /summary endpoint"""
    
    def test_get_summary_success(self, client, mock_summary_service):
        """Test getting summary for existing URL - SUCCESS case"""
        # Arrange
        test_url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
        mock_summary_data = MagicMock()
        mock_summary_data.summary = "Python is a high-level programming language."
        mock_summary_data.url = test_url
        
        mock_summary_service.get_summary_by_url.return_value = mock_summary_data
        
        # Act
        response = client.get(f"/summary/?url2search={quote(test_url)}")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert "summary" in response_data
        assert "url" in response_data
        assert response_data["summary"] == "Python is a high-level programming language."
        assert response_data["url"] == test_url
        mock_summary_service.get_summary_by_url.assert_called_once_with(test_url)
    
    def test_get_summary_not_found(self, client, mock_summary_service):
        """Test getting summary for non-existing URL - FAIL case"""
        # Arrange
        test_url = "https://en.wikipedia.org/wiki/NonExistentPage"
        mock_summary_service.get_summary_by_url.return_value = None
        
        # Act
        response = client.get(f"/summary/?url2search={quote(test_url)}")
        
        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND
        response_data = response.json()
        assert "detail" in response_data
        assert "not found" in response_data["detail"].lower()
        mock_summary_service.get_summary_by_url.assert_called_once_with(test_url)
    
    def test_get_summary_invalid_domain(self, client, mock_summary_service):
        """Test getting summary with non-Wikipedia URL - FAIL case"""
        # Arrange
        test_url = "https://google.com/search"
        
        # Act
        response = client.get(f"/summary/?url2search={quote(test_url)}")
        
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        response_data = response.json()
        assert "detail" in response_data
        assert "wikipedia" in response_data["detail"].lower()
        # Service should not be called for invalid URLs
        mock_summary_service.get_summary_by_url.assert_not_called()
    
    def test_get_summary_missing_url_parameter(self, client):
        """Test getting summary without URL parameter - FAIL case"""
        # Act
        response = client.get("/summary/")
        
        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_get_summary_with_encoded_url(self, client, mock_summary_service):
        """Test getting summary with URL-encoded parameter - SUCCESS case"""
        # Arrange
        test_url = "https://pt.wikipedia.org/wiki/Inteligência_artificial"
        encoded_url = quote(test_url, safe='')
        mock_summary_data = MagicMock()
        mock_summary_data.summary = "AI is intelligence demonstrated by machines."
        mock_summary_data.url = test_url
        
        mock_summary_service.get_summary_by_url.return_value = mock_summary_data
        
        # Act
        response = client.get(f"/summary/?url2search={encoded_url}")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["summary"] == "AI is intelligence demonstrated by machines."
    
    def test_get_summary_with_subdomain_wikipedia(self, client, mock_summary_service):
        """Test getting summary with different Wikipedia subdomain - SUCCESS case"""
        # Arrange
        test_url = "https://es.wikipedia.org/wiki/Machine_learning"
        mock_summary_data = MagicMock()
        mock_summary_data.summary = "Machine learning is a subset of AI."
        mock_summary_data.url = test_url
        
        mock_summary_service.get_summary_by_url.return_value = mock_summary_data
        
        # Act
        response = client.get(f"/summary/?url2search={quote(test_url)}")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["url"] == test_url

