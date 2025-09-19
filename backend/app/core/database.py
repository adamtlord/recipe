import csv
import logging
import os
from contextlib import contextmanager
from typing import Generator

from sqlmodel import Session, SQLModel, create_engine, select

from .config import settings
from ..models.database import Food

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database engine setup
connect_args = {"check_same_thread": False}
engine = create_engine(settings.DATABASE_URL, connect_args=connect_args)


def create_db_and_tables():
    """Create database tables and import initial data."""
    SQLModel.metadata.create_all(engine)
    import_ingredients()


def clear_db_and_tables():
    """Clear database tables and remove database file."""
    if os.path.exists(settings.DATABASE_FILE_NAME):
        try:
            os.remove(settings.DATABASE_FILE_NAME)
            logger.info("Database file deleted successfully")
        except OSError as e:
            logger.exception(f"Error deleting database file: {str(e)}")
    else:
        logger.info("Database file does not exist")


def import_ingredients():
    """Import ingredients from CSV file into the database."""
    csv_file_path = settings.INGREDIENTS_CSV_PATH
    if not os.path.exists(csv_file_path):
        logger.warning(f"Ingredients CSV file not found: {csv_file_path}")
        return

    food_data = []
    with open(csv_file_path, mode="r", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            food_data.append(row)

    with Session(engine) as session:
        for row in food_data:
            food = Food(name=row["descrip"])
            session.add(food)
        session.commit()
        logger.info(f"Imported {len(food_data)} ingredients")


@contextmanager
def get_session() -> Generator[Session, None, None]:
    """Get database session with proper context management."""
    with Session(engine) as session:
        yield session


def select_foods_containing_substring(substr: str, max_results: int = None) -> list[Food]:
    """Search for foods containing the given substring."""
    if max_results is None:
        max_results = settings.MAX_FOOD_RESULTS

    with Session(engine) as session:
        statement = select(Food).where(Food.name.like(f"%{substr}%"))
        results = session.exec(statement).all()
        return results[:max_results]
