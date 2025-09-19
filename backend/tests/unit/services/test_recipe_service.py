import pytest
from unittest.mock import Mock, patch

from app.models.schemas import Recipe, RecipeRequest
from app.services.recipe_service import RecipeService


@pytest.mark.unit
class TestRecipeService:
    """Test cases for the RecipeService."""

    def test_generate_recipe_query_basic(self):
        """Test generating a basic recipe query."""
        request = RecipeRequest(
            ingredients=["chicken", "tomato"],
            max_recipes=2,
            cuisine_style="any"
        )

        query = RecipeService.generate_recipe_query(request)

        expected = "Suggest and provide up to 2 recipes that use the following ingredients: chicken, tomato."
        assert query == expected

    def test_generate_recipe_query_with_cuisine(self):
        """Test generating a recipe query with specific cuisine style."""
        request = RecipeRequest(
            ingredients=["chicken", "tomato", "onion"],
            max_recipes=3,
            cuisine_style="italian"
        )

        query = RecipeService.generate_recipe_query(request)

        expected = "Suggest and provide up to 3 recipes in the style of italian cuisine that use the following ingredients: chicken, tomato, onion."
        assert query == expected

    def test_generate_recipe_query_single_ingredient(self):
        """Test generating a recipe query with single ingredient."""
        request = RecipeRequest(
            ingredients=["chicken"],
            max_recipes=1
        )

        query = RecipeService.generate_recipe_query(request)

        expected = "Suggest and provide up to 1 recipes that use the following ingredients: chicken."
        assert query == expected

    @patch('app.services.recipe_service.client')
    def test_generate_content_success(self, mock_client):
        """Test successful content generation."""
        mock_response = Mock()
        mock_response.parsed = [
            Recipe(
                recipe_name="Test Recipe",
                ingredients=["chicken", "tomato"],
                instructions="Test instructions"
            )
        ]
        mock_client.models.generate_content.return_value = mock_response

        query = "test query"
        result = RecipeService.generate_content(query)

        mock_client.models.generate_content.assert_called_once()
        assert len(result) == 1
        assert result[0].recipe_name == "Test Recipe"

    @patch('app.services.recipe_service.client')
    def test_generate_content_failure(self, mock_client):
        """Test content generation failure."""
        mock_client.models.generate_content.side_effect = Exception("API Error")

        with pytest.raises(Exception, match="API Error"):
            RecipeService.generate_content("test query")

    @patch('app.services.recipe_service.RecipeService.generate_content')
    @patch('app.services.recipe_service.RecipeService.generate_recipe_query')
    def test_generate_recipes_integration(self, mock_query, mock_content):
        """Test the complete generate_recipes workflow."""
        # Setup mocks
        mock_query.return_value = "test query"
        mock_content.return_value = [
            Recipe(
                recipe_name="Test Recipe",
                ingredients=["chicken", "tomato"],
                instructions="Test instructions"
            )
        ]

        request = RecipeRequest(
            ingredients=["chicken", "tomato"],
            max_recipes=1
        )

        result = RecipeService.generate_recipes(request)

        # Verify mocks were called correctly
        mock_query.assert_called_once_with(request)
        mock_content.assert_called_once_with("test query")

        # Verify result
        assert len(result) == 1
        assert result[0].recipe_name == "Test Recipe"
