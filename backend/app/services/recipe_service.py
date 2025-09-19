import logging

from dotenv import load_dotenv
from google import genai

from ..core.config import settings
from ..models.schemas import Recipe, RecipeRequest

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Gemini client
client = genai.Client()

RECIPE_CONFIG = {
    "response_mime_type": "application/json",
    "response_schema": list[Recipe],
}


class RecipeService:
    """Service for handling recipe generation using Gemini AI."""

    @staticmethod
    def generate_recipe_query(request: RecipeRequest) -> str:
        """Generate a query string for recipe generation based on the request."""
        cuisine_clause = ""
        if request.cuisine_style and request.cuisine_style != "any":
            cuisine_clause = f" in the style of {request.cuisine_style} cuisine"

        return (
            f"Suggest and provide up to {request.max_recipes} recipes{cuisine_clause} "
            f"that use the following ingredients: {', '.join(request.ingredients)}."
        )

    @staticmethod
    def generate_content(query: str) -> list[Recipe]:
        """Generate recipe content using Gemini AI."""
        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            config=RECIPE_CONFIG,
            contents=query
        )
        return response.parsed

    @classmethod
    def generate_recipes(cls, request: RecipeRequest) -> list[Recipe]:
        """Generate recipes based on the provided request."""
        query = cls.generate_recipe_query(request)
        return cls.generate_content(query)


# Create service instance
recipe_service = RecipeService()
