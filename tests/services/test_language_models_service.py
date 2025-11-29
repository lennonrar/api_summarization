"""
Tests for LanguageModelsService
"""
import pytest
from unittest.mock import Mock, patch
from langchain_core.documents import Document

from app.services.language_models.language_models import LanguageModelsService, LLMProvider


class TestLanguageModelsService:
    """Test the LanguageModelsService"""

    @pytest.fixture
    def mock_hf_client(self):
        """Create mock HuggingFace InferenceClient"""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.summary_text = "This is a summary."
        mock_client.summarization.return_value = mock_response
        return mock_client

    @pytest.fixture
    def language_models_service(self, mock_hf_client):
        """Create LanguageModelsService with mocked HF client"""
        with patch.dict('os.environ', {'LLM_PROVIDER': 'huggingface', 'HF_TOKEN': 'test_token'}):
            with patch('app.services.language_models.language_models.InferenceClient', return_value=mock_hf_client):
                service = LanguageModelsService()
                return service

    @pytest.mark.asyncio
    async def test_generate_summary_short_text_success(self, language_models_service):
        """Test generating summary for short text - SUCCESS case"""
        # Arrange
        test_text = "Python is a high-level programming language. " * 10
        words_limit = 50

        mock_response = Mock()
        mock_response.summary_text = "Python is a versatile programming language used for various applications."
        language_models_service.client.summarization = Mock(return_value=mock_response)

        # Act
        result = await language_models_service.generate_summary(test_text, words_limit)

        # Assert
        assert isinstance(result, str)
        assert len(result) > 0
        assert result == "Python is a versatile programming language used for various applications."
        language_models_service.client.summarization.assert_called_once()

