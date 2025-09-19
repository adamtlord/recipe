from contextlib import asynccontextmanager

from fastapi import FastAPI

from .api.v1 import foods, recipes
from .core.config import settings
from .core.database import clear_db_and_tables, create_db_and_tables
from .core.security import setup_cors
from .utils.logger import setup_logging

# Setup logging
setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup and shutdown events."""
    # Startup
    create_db_and_tables()
    yield
    # Shutdown
    clear_db_and_tables()


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title=settings.APP_TITLE,
        version=settings.APP_VERSION,
        lifespan=lifespan
    )

    # Setup CORS
    setup_cors(app)

    # Include API routers
    app.include_router(recipes.router, prefix="/api/v1")
    app.include_router(foods.router, prefix="/api/v1")

    # Health check endpoints
    @app.get("/")
    async def root():
        return {"message": "Recipe Suggestion API with Gemini Integration"}

    @app.get("/health")
    async def health_check():
        from .services.recipe_service import client
        return {
            "status": "healthy",
            "api_available": hasattr(client.models, "generate_content"),
        }

    return app


# Create the app instance
app = create_app()