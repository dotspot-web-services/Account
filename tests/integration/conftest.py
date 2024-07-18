import json
import os
from typing import TypeVar
from unittest.mock import create_autospec

import pytest
from sqlalchemy.orm import Session

# from src.user_repository import UserRepository
# from src.user import User


@pytest.fixture(scope="session")
def env_config(request: TypeVar) -> dict[str, str | dict[str, str]]:
    # get config file from different env
    env = os.getenv("ENV", "dev")
    with open(f"config/{env}_config.json", "r") as config_file:
        config = json.load(config_file)
    return config


@pytest.fixture(scope="session")
def request_data(request: TypeVar) -> dict[str, str | dict[str, str]]:
    # get request data file from different env
    env = os.getenv("ENV", "dev")
    with open(f"data/{env}_request_data.json", "r") as request_data_file:
        request_data = json.load(request_data_file)
    return request_data


@pytest.fixture(scope="session")
def response_data(request: TypeVar) -> dict[str, str | dict[str, str]]:
    # get response data file from different env
    env = os.getenv("ENV", "dev")
    with open(f"data/{env}_response_data.json", "r") as response_data_file:
        response_data = json.load(response_data_file)
    return response_data

    # print(accounts.url_map)


@pytest.fixture(scope="session")
def header(token: str) -> dict[str, str]:
    return {"authorization": f"bearer {token}"}


@pytest.fixture
def mock_session() -> Session:
    """Pytest fixture to create a mock Session instance."""
    session = create_autospec(Session)
    return session


def test_get_users(mock_session: Session) -> None:
    """Test the get_users method of the UserRepository class."""
    # Create a fake user
    # fake_user = User(id=1, name="Alice", age=28)

    # Mock the Session.query() method to return our fake user
    # mock_session.query.return_value.all.return_value = [fake_user]

    # Create a UserRepository instance with the mocked session
    # user_repository = UserRepository("postgresql://test:test@test/test")
    # user_repository.session = mock_session

    # TypeVar the get_users method
    # users = user_repository.get_users()

    # Ensure that Session.query() was called with the correct argument
    # mock_session.query.assert_called_with(User)

    # Assert that the method returned our fake user
    # assert users == [fake_user]
