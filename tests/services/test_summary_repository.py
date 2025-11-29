"""
Tests for SummaryRepository
"""
import pytest
from unittest.mock import Mock
from sqlalchemy.orm import Session

from app.services.summary.summary_repository import SummaryRepository
from app.models.summary import Summary


class TestSummaryRepository:
    """Test the SummaryRepository"""

    @pytest.fixture
    def mock_db_session(self):
        """Create mock database session"""
        session = Mock(spec=Session)
        return session

    @pytest.fixture
    def summary_repository(self, mock_db_session):
        """Create SummaryRepository with mocked database session"""
        return SummaryRepository(db=mock_db_session)

    def test_get_summary_by_id_success(self, summary_repository, mock_db_session):
        """Test getting existing summary by ID - SUCCESS case"""
        # Arrange
        test_id = "abc123def456"
        mock_summary = Summary(
            id=test_id,
            url="https://en.wikipedia.org/wiki/Python",
            summary="Python is a programming language."
        )

        mock_query = Mock()
        mock_query.filter.return_value.first.return_value = mock_summary
        mock_db_session.query.return_value = mock_query

        # Act
        result = summary_repository.get_summary_by_id(test_id)

        # Assert
        assert result is not None
        assert result.id == test_id
        assert result.url == "https://en.wikipedia.org/wiki/Python"
        assert result.summary == "Python is a programming language."
        mock_db_session.query.assert_called_once_with(Summary)

    def test_get_summary_by_id_not_found(self, summary_repository, mock_db_session):
        """Test getting non-existing summary by ID - FAIL case"""
        # Arrange
        test_id = "nonexistent123"

        mock_query = Mock()
        mock_query.filter.return_value.first.return_value = None
        mock_db_session.query.return_value = mock_query

        # Act
        result = summary_repository.get_summary_by_id(test_id)

        # Assert
        assert result is None
        mock_db_session.query.assert_called_once_with(Summary)

    def test_create_summary_success(self, summary_repository, mock_db_session):
        """Test creating new summary - SUCCESS case"""
        # Arrange
        test_id = "new123abc456"
        test_url = "https://en.wikipedia.org/wiki/Machine_Learning"
        test_summary = "Machine learning is a subset of AI."

        # Mock the behavior of db operations
        def add_side_effect(obj):
            obj.id = test_id
            obj.url = test_url
            obj.summary = test_summary

        mock_db_session.add.side_effect = add_side_effect
        mock_db_session.commit.return_value = None
        mock_db_session.refresh.return_value = None

        # Act
        result = summary_repository.create_summary(test_id, test_url, test_summary)

        # Assert
        assert result is not None
        assert isinstance(result, Summary)
        mock_db_session.add.assert_called_once()
        mock_db_session.commit.assert_called_once()
        mock_db_session.refresh.assert_called_once()

