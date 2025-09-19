import pytest
from unittest.mock import patch

from app.models.database import Food


@pytest.mark.unit
class TestFoodsAPI:
    """Test cases for the foods API endpoints."""

    def test_search_foods_success(self, test_client):
        """Test successful food search."""
        with patch('app.api.v1.foods.food_service.search_foods') as mock_search:
            mock_search.return_value = [
                Food(id=1, name="chicken breast"),
                Food(id=2, name="chicken thigh")
            ]

            response = test_client.get("/api/v1/foods?q=chicken")

            assert response.status_code == 200
            data = response.json()
            assert len(data) == 2
            assert data[0]["name"] == "chicken breast"
            assert data[1]["name"] == "chicken thigh"

    def test_search_foods_short_query(self, test_client):
        """Test food search with query too short."""
        response = test_client.get("/api/v1/foods?q=ab")

        assert response.status_code == 400
        assert "Enter at least 3 characters" in response.json()["detail"]

    def test_search_foods_empty_query(self, test_client):
        """Test food search with empty query."""
        response = test_client.get("/api/v1/foods?q=")

        assert response.status_code == 400
        assert "Enter at least 3 characters" in response.json()["detail"]

    def test_search_foods_missing_query(self, test_client):
        """Test food search with missing query parameter."""
        response = test_client.get("/api/v1/foods")

        assert response.status_code == 422  # Validation error

    def test_search_foods_no_results(self, test_client):
        """Test food search with no results."""
        with patch('app.api.v1.foods.food_service.search_foods') as mock_search:
            mock_search.return_value = []

            response = test_client.get("/api/v1/foods?q=nonexistent")

            assert response.status_code == 200
            data = response.json()
            assert data == []

    def test_search_foods_service_error(self, test_client):
        """Test food search when service fails."""
        with patch('app.api.v1.foods.food_service.search_foods') as mock_search:
            mock_search.side_effect = Exception("Service error")

            response = test_client.get("/api/v1/foods?q=chicken")

            assert response.status_code == 500
            assert "Failed to search foods" in response.json()["detail"]

    def test_search_foods_whitespace_handling(self, test_client):
        """Test food search with whitespace in query."""
        with patch('app.api.v1.foods.food_service.search_foods') as mock_search:
            mock_search.return_value = []

            response = test_client.get("/api/v1/foods?q=%20chicken%20")

            assert response.status_code == 200
            mock_search.assert_called_once_with(" chicken ")
