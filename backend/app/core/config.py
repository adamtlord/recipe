import os
from typing import List

from dotenv import load_dotenv

load_dotenv()


class Settings:
    # App settings
    APP_TITLE: str = "Recipe Suggestion App"
    APP_VERSION: str = "1.0.0"

    # Database settings
    DATABASE_URL: str = "sqlite:///database.db"
    DATABASE_FILE_NAME: str = "database.db"

    # CORS settings
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:5173",
        "https://recipe-robot-ui.onrender.com",
    ]

    # Gemini AI settings
    GEMINI_MODEL: str = "gemini-2.5-flash"

    # File paths
    INGREDIENTS_CSV_PATH: str = "unique_indexed_ingredients.csv"

    # API settings
    DEFAULT_MAX_RECIPES: int = 3
    DEFAULT_CUISINE_STYLE: str = "any"
    MIN_SEARCH_LENGTH: int = 3
    MAX_FOOD_RESULTS: int = 20


settings = Settings()
