import pytest
from sqlmodel import Session, select

from app.models.database import Food


@pytest.mark.unit
class TestFoodModel:
    """Test cases for the Food database model."""

    def test_food_creation(self, test_session):
        """Test creating a food item."""
        food = Food(name="chicken breast")
        test_session.add(food)
        test_session.commit()
        test_session.refresh(food)

        assert food.id is not None
        assert food.name == "chicken breast"

    def test_food_retrieval(self, test_session):
        """Test retrieving a food item."""
        food = Food(name="tomato")
        test_session.add(food)
        test_session.commit()

        retrieved_food = test_session.get(Food, food.id)
        assert retrieved_food is not None
        assert retrieved_food.name == "tomato"

    def test_food_update(self, test_session):
        """Test updating a food item."""
        food = Food(name="onion")
        test_session.add(food)
        test_session.commit()

        food.name = "red onion"
        test_session.commit()
        test_session.refresh(food)

        assert food.name == "red onion"

    def test_food_deletion(self, test_session):
        """Test deleting a food item."""
        food = Food(name="garlic")
        test_session.add(food)
        test_session.commit()

        food_id = food.id
        test_session.delete(food)
        test_session.commit()

        deleted_food = test_session.get(Food, food_id)
        assert deleted_food is None

    def test_multiple_foods(self, populated_test_session):
        """Test handling multiple food items."""
        foods = populated_test_session.exec(select(Food)).all()
        assert len(foods) == 7  # Based on sample_food_data fixture

        food_names = [food.name for food in foods]
        assert "chicken breast" in food_names
        assert "tomato" in food_names
        assert "onion" in food_names
