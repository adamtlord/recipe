import logging
from contextlib import asynccontextmanager
from typing import List

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models import (
    Food,
    RecipeRequest,
    RecipeResponse,
    clear_db_and_tables,
    create_db_and_tables,
    select_foods_containing_substring,
)
from .recipe import client, generate_content, generate_recipe_query

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    clear_db_and_tables()


app = FastAPI(title="Recipe Suggestion App", version="1.0.0", lifespan=lifespan)

origins = [
    "http://localhost:5173",
    "https://recipe-robot-ui.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Recipe Suggestion API with Gemini Integration"}


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "api_available": hasattr(client.models, "generate_content"),
    }


@app.post("/recipes/generate", response_model=RecipeResponse)
async def generate_recipes(request: RecipeRequest):
    if not request.ingredients:
        raise HTTPException(
            status_code=400, detail="At least one ingredient is required"
        )

    try:
        query = generate_recipe_query(request)
    except Exception as e:
        logger.error(f"Query generation failed: {e}")
        raise HTTPException(
            status_code=400, detail=f"Failed to generate query: {str(e)}"
        )

    try:
        response = generate_content(query)
        return RecipeResponse(recipes=response)

    except Exception as e:
        logger.error(f"Recipe generation failed: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to generate recipes: {str(e)}"
        )


@app.get("/foods", response_model=List[Food])
async def search_foods(q: str | None = None):
    if not q or len(q) < 3:
        raise HTTPException(
            status_code=400, detail="Enter at least three chars to search"
        )

    results = select_foods_containing_substring(q)
    return results
