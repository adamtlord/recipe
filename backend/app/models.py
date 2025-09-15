import csv
import logging
import os
from typing import List

from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine, select

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


class Recipe(BaseModel):
    recipe_name: str
    ingredients: list[str]
    instructions: str


class RecipeRequest(BaseModel):
    ingredients: List[str]
    max_recipes: int = 3
    cuisine_style: str = "any"


class RecipeResponse(BaseModel):
    recipes: List[Recipe]


class Food(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field()


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    import_ingredients()


def clear_db_and_tables():
    if os.path.exists(sqlite_file_name):
        try:
            os.remove(sqlite_file_name)
            logger.info("DB deleted")
        except OSError as e:
            logger.exception(f"Error deleting db file: {str(e)}")
    else:
        logger.info("Database file does not exist")


def import_ingredients():
    csv_file_path = "unique_indexed_ingredients.csv"
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


def get_session():
    with Session(engine) as session:
        yield session


def select_foods_containing_substring(substr: str, max_results: int = 20):
    print("here we go")
    with Session(engine) as session:
        print("session:", session)
        # The '%' acts as a wildcard, matching any sequence of zero or more characters.
        # So, f"%{substring}%" means "substring anywhere in the string".
        statement = select(Food).where(Food.name.like(f"%{substr}%"))
        print(statement)
        results = session.exec(statement).all()
        print(results)

        return results[:max_results]
