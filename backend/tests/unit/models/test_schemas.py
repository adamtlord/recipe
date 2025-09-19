import pytest
from pydantic import ValidationError

from app.models.schemas import Recipe, RecipeRequest, RecipeResponse


@pytest.mark.unit
class TestRecipeSchema:
    """Test cases for the Recipe schema."""

    def test_recipe_creation(self):
        """Test creating a valid recipe."""
        recipe = Recipe(
            recipe_name="Test Recipe",
            ingredients=["ingredient1", "ingredient2"],
            instructions="Test instructions"
        )

        assert recipe.recipe_name == "Test Recipe"
        assert recipe.ingredients == ["ingredient1", "ingredient2"]
        assert recipe.instructions == "Test instructions"

    def test_recipe_validation_errors(self):
        """Test recipe validation with invalid data."""
        # Pydantic allows empty strings by default, so we test with None instead
        with pytest.raises(ValidationError):
            Recipe(
                recipe_name=None,  # None should fail
                ingredients=["ingredient1"],
                instructions="Test instructions"
            )

        # Empty list is allowed by default, so we test with None
        with pytest.raises(ValidationError):
            Recipe(
                recipe_name="Test Recipe",
                ingredients=None,  # None should fail
                instructions="Test instructions"
            )


@pytest.mark.unit
class TestRecipeRequestSchema:
    """Test cases for the RecipeRequest schema."""

    def test_recipe_request_creation(self):
        """Test creating a valid recipe request."""
        request = RecipeRequest(
            ingredients=["chicken", "tomato"],
            max_recipes=5,
            cuisine_style="italian"
        )

        assert request.ingredients == ["chicken", "tomato"]
        assert request.max_recipes == 5
        assert request.cuisine_style == "italian"

    def test_recipe_request_defaults(self):
        """Test recipe request with default values."""
        request = RecipeRequest(ingredients=["chicken"])

        assert request.max_recipes == 3  # Default value
        assert request.cuisine_style == "any"  # Default value

    def test_recipe_request_validation(self):
        """Test recipe request validation."""
        with pytest.raises(ValidationError):
            RecipeRequest(ingredients=None)  # None ingredients should fail


@pytest.mark.unit
class TestRecipeResponseSchema:
    """Test cases for the RecipeResponse schema."""

    def test_recipe_response_creation(self, sample_recipes):
        """Test creating a valid recipe response."""
        recipes = [Recipe(**recipe_data) for recipe_data in sample_recipes]
        response = RecipeResponse(recipes=recipes)

        assert len(response.recipes) == 2
        assert response.recipes[0].recipe_name == "Chicken Tomato Pasta"
        assert response.recipes[1].recipe_name == "Chicken Stir Fry"

    def test_recipe_response_empty_list(self):
        """Test recipe response with empty recipes list."""
        response = RecipeResponse(recipes=[])

        assert response.recipes == []
