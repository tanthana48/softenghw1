import pytest

from app import app
from src.vending.vending_machine import action_query, select_query


def test_select_query():
    # Test select_query with valid input
    with app.app_context():
        result = select_query("SELECT * FROM product")
        assert result is not None

    # Test select_query with invalid input
    with pytest.raises(Exception) as e:
        action_query("INVALID SQL STATEMENT")
        assert str(e) == "Invalid SQL statement: INVALID SQL STATEMENT"


def test_action_query():
    # Test action_query with valid input
    with app.app_context():
        result = action_query("UPDATE machine SET machine_name = 'test_action_query' WHERE id = 1")
        assert result == {"message": "Success"}

    # Test action_query with invalid input
    with pytest.raises(Exception) as e:
        action_query("INVALID SQL STATEMENT")
        assert str(e) == "Invalid SQL statement: INVALID SQL STATEMENT"
