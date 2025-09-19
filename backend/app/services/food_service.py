import logging
from typing import List

from ..core.database import select_foods_containing_substring
from ..core.config import settings
from ..models.database import Food

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FoodService:
    """Service for handling food/ingredient search operations."""

    @staticmethod
    def search_foods(query: str, max_results: int = None) -> List[Food]:
        """Search for foods containing the given query string."""
        if max_results is None:
            max_results = settings.MAX_FOOD_RESULTS

        return select_foods_containing_substring(query, max_results)

    @staticmethod
    def validate_search_query(query: str) -> bool:
        """Validate that the search query meets minimum requirements."""
        return query and len(query.strip()) >= settings.MIN_SEARCH_LENGTH


# Create service instance
food_service = FoodService()
