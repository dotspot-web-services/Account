from typing import Dict

import pytest
import requests


class TestPytestMultiEnvDemo:
    @pytest.mark.Regression  # mark the test case as regression
    def test_get_demo_filter(
        self,
        env_config: Dict[str, str],
        request_data: Dict[str, str],
        response_data: Dict[str, str],
    ) -> None:
        host = env_config["host"]
        get_api = env_config["getAPI"]
        get_api_response_data = response_data["getAPI"]
        # send request
        response = requests.get(host + get_api)
        # assert
        assert response.status_code == 200
        assert response.json() == get_api_response_data

    @pytest.mark.Smoke  # mark the test case as smoke
    def test_post_demo_filter(
        self,
        env_config: Dict[str, str],
        request_data: Dict[str, str],
        response_data: Dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["postAPI"]
        post_api_request_data = request_data["postAPI"]
        print("make the request")
        post_api_response_data = response_data["postAPI"]
        # Your test code here
        response = requests.post(host + post_api, json=post_api_request_data)
        print("verify the response status code")
        assert response.status_code == 201
        print("verify the response data")
        assert response.json() == post_api_response_data
