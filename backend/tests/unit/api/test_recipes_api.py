import pytest
from unittest.mock import patch

from app.models.schemas import Recipe


@pytest.mark.unit
class TestRecipesAPI:
    """Test cases for the recipes API endpoints."""

    def test_generate_recipes_success(self, test_client):
        """Test successful recipe generation."""
        with patch('app.api.v1.recipes.recipe_service.generate_recipes') as mock_generate:
            mock_generate.return_value = [
                Recipe(
                    recipe_name="Test Recipe",
                    ingredients=["chicken", "tomato"],
                    instructions="Test instructions"
                )
            ]

            response = test_client.post(
                "/api/v1/recipes/generate",
                json={
                    "ingredients": ["chicken", "tomato"],
                    "max_recipes": 1,
                    "cuisine_style": "italian"
                }
            )

            assert response.status_code == 200
            data = response.json()
            assert "recipes" in data
            assert len(data["recipes"]) == 1
            assert data["recipes"][0]["recipe_name"] == "Test Recipe"

    def test_generate_recipes_empty_ingredients(self, test_client):
        """Test recipe generation with empty ingredients."""
        response = test_client.post(
            "/api/v1/recipes/generate",
            json={
                "ingredients": [],
                "max_recipes": 1
            }
        )

        assert response.status_code == 400
        assert "At least one ingredient is required" in response.json()["detail"]

    def test_generate_recipes_missing_ingredients(self, test_client):
        """Test recipe generation with missing ingredients field."""
        response = test_client.post(
            "/api/v1/recipes/generate",
            json={
                "max_recipes": 1
            }
        )

        assert response.status_code == 422  # Validation error

    def test_generate_recipes_service_error(self, test_client):
        """Test recipe generation when service fails."""
        with patch('app.api.v1.recipes.recipe_service.generate_recipes') as mock_generate:
            mock_generate.side_effect = Exception("Service error")

            response = test_client.post(
                "/api/v1/recipes/generate",
                json={
                    "ingredients": ["chicken"],
                    "max_recipes": 1
                }
            )

            assert response.status_code == 500
            assert "Failed to generate recipes" in response.json()["detail"]

    def test_generate_recipes_default_values(self, test_client):
        """Test recipe generation with default values."""
        with patch('app.api.v1.recipes.recipe_service.generate_recipes') as mock_generate:
            mock_generate.return_value = []

            response = test_client.post(
                "/api/v1/recipes/generate",
                json={
                    "ingredients": ["chicken"]
                }
            )

            assert response.status_code == 200
            # Verify that the service was called with default values
            mock_generate.assert_called_once()
            call_args = mock_generate.call_args[0][0]
            assert call_args.max_recipes == 3  # Default value
            assert call_args.cuisine_style == "any"  # Default value
