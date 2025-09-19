import logging
from typing import List

from fastapi import APIRouter, HTTPException, Query

from ...core.config import settings
from ...models.database import Food
from ...services.food_service import food_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/foods", tags=["foods"])


@router.get("", response_model=List[Food])
async def search_foods(q: str = Query(..., description="Search query for food ingredients")):
    """Search for food ingredients containing the given query string."""
    if not food_service.validate_search_query(q):
        raise HTTPException(
            status_code=400,
            detail=f"Enter at least {settings.MIN_SEARCH_LENGTH} characters to search"
        )

    try:
        results = food_service.search_foods(q)
        return results
    except Exception as e:
        logger.error(f"Food search failed: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to search foods: {str(e)}"
        )
