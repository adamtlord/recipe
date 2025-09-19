from typing import List

from pydantic import BaseModel


class Recipe(BaseModel):
    """Schema for recipe data."""
    recipe_name: str
    ingredients: list[str]
    instructions: str


class RecipeRequest(BaseModel):
    """Schema for recipe generation request."""
    ingredients: List[str]
    max_recipes: int = 3
    cuisine_style: str = "any"


class RecipeResponse(BaseModel):
    """Schema for recipe generation response."""
    recipes: List[Recipe]
