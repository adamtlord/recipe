import pytest
from unittest.mock import patch

from app.models.database import Food
from app.services.food_service import FoodService


@pytest.mark.unit
class TestFoodService:
    """Test cases for the FoodService."""

    def test_validate_search_query_valid(self):
        """Test validating a valid search query."""
        assert FoodService.validate_search_query("chicken") is True
        assert FoodService.validate_search_query("tom") is True
        assert FoodService.validate_search_query("   valid   ") is True

    def test_validate_search_query_invalid(self):
        """Test validating invalid search queries."""
        assert not FoodService.validate_search_query("")  # Empty string is falsy
        assert not FoodService.validate_search_query("ab")  # Less than 3 chars
        assert not FoodService.validate_search_query("  ")  # Less than 3 chars (whitespace)
        assert not FoodService.validate_search_query(None)  # None is falsy

    @patch('app.services.food_service.select_foods_containing_substring')
    def test_search_foods_success(self, mock_select):
        """Test successful food search."""
        mock_foods = [
            Food(id=1, name="chicken breast"),
            Food(id=2, name="chicken thigh")
        ]
        mock_select.return_value = mock_foods

        result = FoodService.search_foods("chicken")

        mock_select.assert_called_once_with("chicken", 20)  # Default max_results from settings
        assert len(result) == 2
        assert result[0].name == "chicken breast"
        assert result[1].name == "chicken thigh"

    @patch('app.services.food_service.select_foods_containing_substring')
    def test_search_foods_with_max_results(self, mock_select):
        """Test food search with custom max results."""
        mock_foods = [Food(id=1, name="chicken breast")]
        mock_select.return_value = mock_foods

        result = FoodService.search_foods("chicken", max_results=5)

        mock_select.assert_called_once_with("chicken", 5)
        assert len(result) == 1

    @patch('app.services.food_service.select_foods_containing_substring')
    def test_search_foods_empty_result(self, mock_select):
        """Test food search with no results."""
        mock_select.return_value = []

        result = FoodService.search_foods("nonexistent")

        assert result == []

    @patch('app.services.food_service.select_foods_containing_substring')
    def test_search_foods_database_error(self, mock_select):
        """Test food search with database error."""
        mock_select.side_effect = Exception("Database error")

        with pytest.raises(Exception, match="Database error"):
            FoodService.search_foods("chicken")
