import json
import os
from typing import TypeVar
import requests

import pytest
from sqlalchemy.orm import Session

# from src.user_repository import UserRepository
# from src.user import User


# @pytest.fixture(scope="session")
def env_config() -> dict[str, str | dict[str, str]]:
    # get config file from different env
    env = os.getenv("ENV", "dev")
    with open(f"config/{env}_config.json", "r") as config_file:
        config = json.load(config_file)
        # print(config)
    return config


# @pytest.fixture(scope="session")
def request_data() -> dict[str, str | dict[str, str]]:
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
def user_one(
    env_config: dict[str, str],
    request_data: dict[str, str],
) -> dict[str, str]:
    host = env_config["host"]
    post_api = env_config["regAPI"]
    post_api_request_data = request_data["regAPI"]
    print("make the request")
    # Your test code here
    print(post_api_request_data[0])
    response = requests.post(host + post_api, json=post_api_request_data[0])
    print(response)
    token = response
    print(token)
    return {"authorization": f"bearer {token}"}


@pytest.fixture(scope="session")
def usr_two(
    env_config: dict[str, str],
    request_data: dict[str, str],
) -> dict[str, str]:
    host = env_config["host"]
    post_api = env_config["regAPI"]
    post_api_request_data = request_data["regAPI"]
    print("make the request")
    # Your test code here
    response = requests.post(host + post_api, json=post_api_request_data[1])
    token = response
    print(token)
    return {"authorization": f"bearer {token}"}


# @pytest.fixture
# def mock_session() -> Session:
#    """Pytest fixture to create a mock Session instance."""
#    session = create_autospec(Session)
#    return session


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


# if __name__ == "__main__":
#    conf_data: dict[str, str | dict[str, str]] = env_config()
#    data: str | dict[str, str] | None = request_data().get("regAPI")
#    # print(data[0])
#    resp = requests.post(
#        url=conf_data.get("host") + conf_data.get("regAPI"), data=data[0]
#    )
#    print(resp.status_code)
#
