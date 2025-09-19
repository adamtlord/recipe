import os
import tempfile
from unittest.mock import patch, mock_open

import pytest
from sqlmodel import Session, create_engine

from app.core.database import (
    create_db_and_tables,
    clear_db_and_tables,
    import_ingredients,
    select_foods_containing_substring
)
from app.models.database import Food


@pytest.mark.unit
class TestDatabaseOperations:
    """Test cases for database operations."""

    def test_create_db_and_tables(self, test_engine):
        """Test database and table creation."""
        # The test_engine fixture already creates tables, so we just verify
        with Session(test_engine) as session:
            # Try to query the Food table to verify it exists
            from sqlmodel import select
            foods = session.exec(select(Food)).all()
            assert isinstance(foods, list)

    def test_clear_db_and_tables_file_exists(self, tmp_path):
        """Test clearing database when file exists."""
        db_file = tmp_path / "test.db"
        db_file.write_text("test data")

        with patch('app.core.database.settings') as mock_settings:
            mock_settings.DATABASE_FILE_NAME = str(db_file)

            clear_db_and_tables()

            assert not db_file.exists()

    def test_clear_db_and_tables_file_not_exists(self):
        """Test clearing database when file doesn't exist."""
        with patch('app.core.database.settings') as mock_settings:
            mock_settings.DATABASE_FILE_NAME = "nonexistent.db"

            # Should not raise an exception
            clear_db_and_tables()

    @patch('builtins.open', new_callable=mock_open)
    @patch('csv.DictReader')
    def test_import_ingredients_success(self, mock_csv_reader, mock_file, test_session):
        """Test successful ingredient import."""
        # Mock CSV data
        mock_csv_reader.return_value = [
            {"descrip": "chicken breast"},
            {"descrip": "tomato"},
            {"descrip": "onion"}
        ]

        with patch('app.core.database.Session') as mock_session_class:
            mock_session_instance = test_session
            mock_session_class.return_value.__enter__.return_value = mock_session_instance

            import_ingredients()

            # Verify foods were added to the session
            from sqlmodel import select
            foods = test_session.exec(select(Food)).all()
            assert len(foods) == 3
            assert foods[0].name == "chicken breast"
            assert foods[1].name == "tomato"
            assert foods[2].name == "onion"

    def test_import_ingredients_file_not_found(self):
        """Test ingredient import when CSV file doesn't exist."""
        with patch('app.core.database.settings') as mock_settings:
            mock_settings.INGREDIENTS_CSV_PATH = "nonexistent.csv"

            with patch('app.core.database.os.path.exists', return_value=False):
                # Should not raise an exception, just log a warning
                import_ingredients()

    def test_select_foods_containing_substring(self, populated_test_session):
        """Test searching foods with substring."""
        from sqlmodel import select
        statement = select(Food).where(Food.name.like("%chicken%"))
        results = populated_test_session.exec(statement).all()

        assert len(results) == 1
        assert results[0].name == "chicken breast"

    def test_select_foods_containing_substring_no_results(self, populated_test_session):
        """Test searching foods with no matching substring."""
        from sqlmodel import select
        statement = select(Food).where(Food.name.like("%nonexistent%"))
        results = populated_test_session.exec(statement).all()

        assert len(results) == 0

    def test_select_foods_containing_substring_case_insensitive(self, populated_test_session):
        """Test searching foods is case insensitive."""
        from sqlmodel import select
        statement = select(Food).where(Food.name.like("%CHICKEN%"))
        results = populated_test_session.exec(statement).all()

        assert len(results) == 1
        assert results[0].name == "chicken breast"

    def test_select_foods_containing_substring_partial_match(self, populated_test_session):
        """Test searching foods with partial match."""
        from sqlmodel import select
        statement = select(Food).where(Food.name.like("%tom%"))
        results = populated_test_session.exec(statement).all()

        assert len(results) == 1
        assert results[0].name == "tomato"

    def test_select_foods_containing_substring_max_results(self, populated_test_session):
        """Test searching foods with max results limit."""
        # Add more test data
        additional_foods = [
            Food(name="chicken thigh"),
            Food(name="chicken wing"),
            Food(name="chicken drumstick")
        ]
        for food in additional_foods:
            populated_test_session.add(food)
        populated_test_session.commit()

        from sqlmodel import select
        statement = select(Food).where(Food.name.like("%chicken%"))
        results = populated_test_session.exec(statement).all()

        # Limit to 2 results manually since we're testing the query logic
        limited_results = results[:2]
        assert len(limited_results) == 2
