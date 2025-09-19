import logging
from typing import List

from fastapi import APIRouter, HTTPException

from ...models.schemas import RecipeRequest, RecipeResponse
from ...services.recipe_service import recipe_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/recipes", tags=["recipes"])


@router.post("/generate", response_model=RecipeResponse)
async def generate_recipes(request: RecipeRequest):
    """Generate recipes based on provided ingredients."""
    if not request.ingredients:
        raise HTTPException(
            status_code=400, detail="At least one ingredient is required"
        )

    try:
        recipes = recipe_service.generate_recipes(request)
        return RecipeResponse(recipes=recipes)

    except Exception as e:
        logger.error(f"Recipe generation failed: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to generate recipes: {str(e)}"
        )
