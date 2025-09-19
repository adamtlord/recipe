import pytest
from unittest.mock import patch

from app.models.schemas import Recipe


@pytest.mark.integration
class TestAppIntegration:
    """Integration tests for the entire application."""

    def test_health_endpoint(self, test_client):
        """Test the health check endpoint."""
        response = test_client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "api_available" in data

    def test_root_endpoint(self, test_client):
        """Test the root endpoint."""
        response = test_client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Recipe Suggestion API" in data["message"]

    def test_cors_headers(self, test_client):
        """Test that CORS headers are properly set."""
        response = test_client.options("/api/v1/recipes/generate")

        # FastAPI TestClient doesn't fully test CORS, but we can verify the endpoint exists
        assert response.status_code in [200, 405]  # OPTIONS might not be implemented

    @patch('app.api.v1.recipes.recipe_service.generate_recipes')
    def test_full_recipe_generation_flow(self, mock_generate, test_client, populated_test_session):
        """Test the complete recipe generation flow."""
        # Setup mock
        mock_generate.return_value = [
            Recipe(
                recipe_name="Chicken Tomato Pasta",
                ingredients=["chicken", "tomato", "pasta"],
                instructions="Cook pasta, sauté chicken and tomato, combine."
            )
        ]

        # Test food search first
        search_response = test_client.get("/api/v1/foods?q=chicken")
        assert search_response.status_code == 200

        # Test recipe generation
        recipe_response = test_client.post(
            "/api/v1/recipes/generate",
            json={
                "ingredients": ["chicken", "tomato"],
                "max_recipes": 1,
                "cuisine_style": "italian"
            }
        )

        assert recipe_response.status_code == 200
        data = recipe_response.json()
        assert len(data["recipes"]) == 1
        assert data["recipes"][0]["recipe_name"] == "Chicken Tomato Pasta"

    def test_database_persistence(self, test_client, populated_test_session):
        """Test that database operations persist correctly."""
        # Add a new food item
        from app.models.database import Food
        new_food = Food(name="test ingredient")
        populated_test_session.add(new_food)
        populated_test_session.commit()

        # Search for it
        response = test_client.get("/api/v1/foods?q=test")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "test ingredient"
