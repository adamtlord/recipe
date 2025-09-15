import logging

from dotenv import load_dotenv
from google import genai

from .models import Recipe, RecipeRequest

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


client = genai.Client()

MODEL = "gemini-2.5-flash"
RECIPE_CONFIG = {
    "response_mime_type": "application/json",
    "response_schema": list[Recipe],
}


def generate_recipe_query(request: RecipeRequest) -> str:
    cuisine_clause = ""
    if request.cuisine_style:
        cuisine_clause += f"in the style of {request.cuisine_style} cuisine"
    return f"Suggest and provide up to {request.max_recipes} recipes {cuisine_clause} that use the following ingredients: {', '.join(request.ingredients)}."


def generate_content(query: str) -> str:
    response = client.models.generate_content(
        model=MODEL, config=RECIPE_CONFIG, contents=query
    )

    return response.parsed
