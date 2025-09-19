import os
import tempfile
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.main import create_app
from app.core.database import get_session
from app.models.database import Food


@pytest.fixture(scope="session")
def test_db_url():
    """Create a temporary database URL for testing."""
    # Create a temporary file for the test database
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    os.close(db_fd)
    yield f"sqlite:///{db_path}"
    # Clean up
    if os.path.exists(db_path):
        os.unlink(db_path)


@pytest.fixture(scope="function")
def test_engine(test_db_url):
    """Create a test database engine."""
    engine = create_engine(
        test_db_url,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def test_session(test_engine):
    """Create a test database session."""
    with Session(test_engine) as session:
        yield session


@pytest.fixture(scope="function")
def test_client(test_engine):
    """Create a test client with a test database."""
    def get_test_session():
        with Session(test_engine) as session:
            yield session

    # Create app without lifespan to avoid database conflicts
    from fastapi import FastAPI
    from app.core.config import settings
    from app.core.security import setup_cors
    from app.api.v1 import foods, recipes

    app = FastAPI(
        title=settings.APP_TITLE,
        version=settings.APP_VERSION
    )

    # Setup CORS
    setup_cors(app)

    # Include API routers
    app.include_router(recipes.router, prefix="/api/v1")
    app.include_router(foods.router, prefix="/api/v1")

    # Override database dependency
    app.dependency_overrides[get_session] = get_test_session

    # Add basic endpoints
    @app.get("/")
    async def root():
        return {"message": "Recipe Suggestion API with Gemini Integration"}

    @app.get("/health")
    async def health_check():
        return {
            "status": "healthy",
            "api_available": True,
        }

    with TestClient(app) as client:
        yield client


@pytest.fixture
def sample_food_data():
    """Sample food data for testing."""
    return [
        {"name": "chicken breast"},
        {"name": "tomato"},
        {"name": "onion"},
        {"name": "garlic"},
        {"name": "olive oil"},
        {"name": "salt"},
        {"name": "black pepper"},
    ]


@pytest.fixture
def populated_test_session(test_session, sample_food_data):
    """Test session with sample food data."""
    for food_data in sample_food_data:
        food = Food(**food_data)
        test_session.add(food)
    test_session.commit()
    return test_session


@pytest.fixture
def sample_recipe_request():
    """Sample recipe request for testing."""
    return {
        "ingredients": ["chicken breast", "tomato", "onion"],
        "max_recipes": 2,
        "cuisine_style": "italian"
    }


@pytest.fixture
def sample_recipes():
    """Sample recipe data for testing."""
    return [
        {
            "recipe_name": "Chicken Tomato Pasta",
            "ingredients": ["chicken breast", "tomato", "onion", "pasta"],
            "instructions": "Cook pasta, sauté chicken and vegetables, combine."
        },
        {
            "recipe_name": "Chicken Stir Fry",
            "ingredients": ["chicken breast", "onion", "garlic", "soy sauce"],
            "instructions": "Stir fry chicken with vegetables and sauce."
        }
    ]
