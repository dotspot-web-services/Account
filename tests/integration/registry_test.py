import pytest
import requests


class TestRegistryMultiEnv:
    @pytest.mark.Regression  # mark the test case as regression
    def test_registry_get_200_ok(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        print(host)
        get_api = env_config["regAPI"]
        get_api_response_data = response_data["regAPI"]
        # send request
        response = requests.get(host + get_api, headers=user_one)
        # assert
        assert response.status_code == 200
        assert response.json() == get_api_response_data

    @pytest.mark.Regression  # mark the test case as regression
    def test_registry_get_401_unauthorized(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        get_api = env_config["regAPI"]
        get_api_response_data = response_data["regAPI"]
        # send request
        response = requests.get(host + get_api, headers=user_one)
        # assert
        assert response.status_code == 401
        assert response.json() == get_api_response_data

    @pytest.mark.Regression  # mark the test case as regression
    def test_registry_get_404_not_found(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        get_api = env_config["regAPI"]
        get_api_response_data = response_data["regAPI"]
        # send request
        response = requests.get(host + get_api, headers=user_one)
        # assert
        assert response.status_code == 404
        assert response.json() == get_api_response_data

    # POST test starts
    @pytest.mark.Smoke  # mark the test case as smoke
    def test_registry_post_200_ok(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["regAPI"]
        post_api_request_data = request_data["regAPI"]
        print("make the request")
        post_api_response_data = response_data["regAPI"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=user_one
        )
        print("verify the response status code")
        assert response.status_code == 201
        print("verify the response data")
        assert response.json() == post_api_response_data

    @pytest.mark.Smoke  # mark the test case as smoke
    def test_registry_post_401_unauthorized(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["regAPI"]
        post_api_request_data = request_data["regAPI"]
        print("make the request")
        post_api_response_data = response_data["regAPI"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=user_one
        )
        print("verify the response status code")
        assert response.status_code == 401
        print("verify the response data")
        assert response.json() == post_api_response_data

    @pytest.mark.Smoke  # mark the test case as smoke
    def test_registry_post_422_data_error(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["regAPI"]
        post_api_request_data = request_data["regAPI"]
        print("make the request")
        post_api_response_data = response_data["regAPI"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=user_one
        )
        print("verify the response status code")
        assert response.status_code == 422
        print("verify the response data")
        assert response.json() == post_api_response_data

    @pytest.mark.Smoke  # mark the test case as smoke
    def test_registry_post_404_not_found(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["regAPI"]
        post_api_request_data = request_data["regAPI"]
        print("make the request")
        post_api_response_data = response_data["regAPI"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=user_one
        )
        print("verify the response status code")
        assert response.status_code == 404
        print("verify the response data")
        assert response.json() == post_api_response_data

    # PUT Test Starts Here
    @pytest.mark.Smoke  # mark the test case as smoke
    def test_registry_put_200_ok(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["regAPI"]
        post_api_request_data = request_data["regAPI"]
        print("make the request")
        post_api_response_data = response_data["regAPI"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=user_one
        )
        print("verify the response status code")
        assert response.status_code == 201
        print("verify the response data")
        assert response.json() == post_api_response_data

    @pytest.mark.Smoke  # mark the test case as smoke
    def test_registry_put_401_unauthorized(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["regAPI"]
        post_api_request_data = request_data["regAPI"]
        print("make the request")
        post_api_response_data = response_data["regAPI"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=user_one
        )
        print("verify the response status code")
        assert response.status_code == 401
        print("verify the response data")
        assert response.json() == post_api_response_data

    @pytest.mark.Smoke  # mark the test case as smoke
    def test_registry_put_422_data_error(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["regAPI"]
        post_api_request_data = request_data["regAPI"]
        print("make the request")
        post_api_response_data = response_data["regAPI"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=user_one
        )
        print("verify the response status code")
        assert response.status_code == 422
        print("verify the response data")
        assert response.json() == post_api_response_data

    @pytest.mark.Smoke  # mark the test case as smoke
    def test_registry_put_404_not_found(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["regAPI"]
        post_api_request_data = request_data["regAPI"]
        print("make the request")
        post_api_response_data = response_data["regAPI"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=user_one
        )
        print("verify the response status code")
        assert response.status_code == 404
        print("verify the response data")
        assert response.json() == post_api_response_data


# LOGIN RESTFUL API TEST STARTS HERE
class TestLoginMultiEnv:
    @pytest.mark.Regression  # mark the test case as regression
    def test_login_get_200_ok(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        get_api = env_config["login"]
        get_api_response_data = response_data["login"]
        # send request
        response = requests.get(host + get_api, headers=user_one)
        # assert
        assert response.status_code == 200
        assert response.json() == get_api_response_data

    @pytest.mark.Regression  # mark the test case as regression
    def test_login_get_401_unauthorized(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        get_api = env_config["login"]
        get_api_response_data = response_data["login"]
        # send request
        response = requests.get(host + get_api, headers=user_one)
        # assert
        assert response.status_code == 401
        assert response.json() == get_api_response_data

    @pytest.mark.Regression  # mark the test case as regression
    def test_login_get_404_not_found(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        get_api = env_config["login"]
        get_api_response_data = response_data["login"]
        # send request
        response = requests.get(host + get_api, headers=user_one)
        # assert
        assert response.status_code == 404
        assert response.json() == get_api_response_data

    # POST test starts
    @pytest.mark.Smoke  # mark the test case as smoke
    def test_login_post_200_ok(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["login"]
        post_api_request_data = request_data["login"]
        print("make the request")
        post_api_response_data = response_data["login"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=user_one
        )
        print("verify the response status code")
        assert response.status_code == 201
        print("verify the response data")
        assert response.json() == post_api_response_data

    @pytest.mark.Smoke  # mark the test case as smoke
    def test_login_post_401_unauthorized(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["login"]
        post_api_request_data = request_data["login"]
        print("make the request")
        post_api_response_data = response_data["login"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=user_one
        )
        print("verify the response status code")
        assert response.status_code == 401
        print("verify the response data")
        assert response.json() == post_api_response_data

    @pytest.mark.Smoke  # mark the test case as smoke
    def test_login_post_422_data_error(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["login"]
        post_api_request_data = request_data["login"]
        print("make the request")
        post_api_response_data = response_data["login"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=user_one
        )
        print("verify the response status code")
        assert response.status_code == 422
        print("verify the response data")
        assert response.json() == post_api_response_data

    @pytest.mark.Smoke  # mark the test case as smoke
    def test_login_post_404_not_found(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["login"]
        post_api_request_data = request_data["login"]
        print("make the request")
        post_api_response_data = response_data["login"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=user_one
        )
        print("verify the response status code")
        assert response.status_code == 404
        print("verify the response data")
        assert response.json() == post_api_response_data

    # PUT Test Starts Here
    @pytest.mark.Smoke  # mark the test case as smoke
    def test_login_put_200_ok(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["login"]
        post_api_request_data = request_data["login"]
        print("make the request")
        post_api_response_data = response_data["login"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=user_one
        )
        print("verify the response status code")
        assert response.status_code == 201
        print("verify the response data")
        assert response.json() == post_api_response_data

    @pytest.mark.Smoke  # mark the test case as smoke
    def test_login_put_401_unauthorized(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["login"]
        post_api_request_data = request_data["login"]
        print("make the request")
        post_api_response_data = response_data["login"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=user_one
        )
        print("verify the response status code")
        assert response.status_code == 401
        print("verify the response data")
        assert response.json() == post_api_response_data

    @pytest.mark.Smoke  # mark the test case as smoke
    def test_login_put_422_data_error(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["login"]
        post_api_request_data = request_data["login"]
        print("make the request")
        post_api_response_data = response_data["login"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=user_one
        )
        print("verify the response status code")
        assert response.status_code == 422
        print("verify the response data")
        assert response.json() == post_api_response_data

    @pytest.mark.Smoke  # mark the test case as smoke
    def test_login_put_404_not_found(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["login"]
        post_api_request_data = request_data["login"]
        print("make the request")
        post_api_response_data = response_data["login"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=user_one
        )
        print("verify the response status code")
        assert response.status_code == 404
        print("verify the response data")
        assert response.json() == post_api_response_data

    # DELETE Starts Here
    @pytest.mark.Regression  # mark the test case as regression
    def test_login_delte_200_ok(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        get_api = env_config["login"]
        get_api_response_data = response_data["login"]
        # send request
        response = requests.get(host + get_api, headers=user_one)
        # assert
        assert response.status_code == 200
        assert response.json() == get_api_response_data

    @pytest.mark.Regression  # mark the test case as regression
    def test_login_delete_401_unauthorized(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        get_api = env_config["login"]
        get_api_response_data = response_data["login"]
        # send request
        response = requests.get(host + get_api, headers=user_one)
        # assert
        assert response.status_code == 401
        assert response.json() == get_api_response_data

    @pytest.mark.Regression  # mark the test case as regression
    def test_login_delete_404_not_found(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        get_api = env_config["login"]
        get_api_response_data = response_data["login"]
        # send request
        response = requests.get(host + get_api, headers=user_one)
        # assert
        assert response.status_code == 404
        assert response.json() == get_api_response_data


# LOGOUT RESTFUL API TEST STARTS HERE
class TestLOGOUTMultiEnv:
    @pytest.mark.Regression  # mark the test case as regression
    def test_logout_get_200_ok(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        get_api = env_config["logout"]
        get_api_response_data = response_data["logout"]
        # send request
        response = requests.get(host + get_api, headers=user_one)
        # assert
        assert response.status_code == 200
        assert response.json() == get_api_response_data

    @pytest.mark.Regression  # mark the test case as regression
    def test_logout_get_401_unauthorized(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        get_api = env_config["logout"]
        get_api_response_data = response_data["logout"]
        # send request
        response = requests.get(host + get_api, headers=user_one)
        # assert
        assert response.status_code == 401
        assert response.json() == get_api_response_data

    @pytest.mark.Regression  # mark the test case as regression
    def test_logout_get_404_not_found(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        get_api = env_config["logout"]
        get_api_response_data = response_data["logout"]
        # send request
        response = requests.get(host + get_api, headers=user_one)
        # assert
        assert response.status_code == 404
        assert response.json() == get_api_response_data

    # POST test starts
    @pytest.mark.Smoke  # mark the test case as smoke
    def test_logout_post_200_ok(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["logout"]
        post_api_request_data = request_data["logout"]
        print("make the request")
        post_api_response_data = response_data["logout"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=user_one
        )
        print("verify the response status code")
        assert response.status_code == 201
        print("verify the response data")
        assert response.json() == post_api_response_data

    @pytest.mark.Smoke  # mark the test case as smoke
    def test_logout_post_401_unauthorized(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["logout"]
        post_api_request_data = request_data["logout"]
        print("make the request")
        post_api_response_data = response_data["logout"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=user_one
        )
        print("verify the response status code")
        assert response.status_code == 401
        print("verify the response data")
        assert response.json() == post_api_response_data

    @pytest.mark.Smoke  # mark the test case as smoke
    def test_logout_post_422_data_error(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["logout"]
        post_api_request_data = request_data["logout"]
        print("make the request")
        post_api_response_data = response_data["logout"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=user_one
        )
        print("verify the response status code")
        assert response.status_code == 422
        print("verify the response data")
        assert response.json() == post_api_response_data

    @pytest.mark.Smoke  # mark the test case as smoke
    def test_logout_post_404_not_found(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["logout"]
        post_api_request_data = request_data["logout"]
        print("make the request")
        post_api_response_data = response_data["logout"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=user_one
        )
        print("verify the response status code")
        assert response.status_code == 404
        print("verify the response data")
        assert response.json() == post_api_response_data


# RESET RESTFUL API TEST STARTS HERE
class TestWorkMultiEnv:
    @pytest.mark.Regression  # mark the test case as regression
    def test_reset_get_200_ok(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        get_api = env_config["rese"]
        get_api_response_data = response_data["rese"]
        # send request
        response = requests.get(host + get_api, headers=user_one)
        # assert
        assert response.status_code == 200
        assert response.json() == get_api_response_data

    @pytest.mark.Regression  # mark the test case as regression
    def test_reset_get_401_unauthorized(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        get_api = env_config["rese"]
        get_api_response_data = response_data["rese"]
        # send request
        response = requests.get(host + get_api, headers=user_one)
        # assert
        assert response.status_code == 401
        assert response.json() == get_api_response_data

    @pytest.mark.Regression  # mark the test case as regression
    def test_reset_get_404_not_found(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        get_api = env_config["rese"]
        get_api_response_data = response_data["rese"]
        # send request
        response = requests.get(host + get_api, headers=user_one)
        # assert
        assert response.status_code == 404
        assert response.json() == get_api_response_data

    # POST test starts
    @pytest.mark.Smoke  # mark the test case as smoke
    def test_reset_post_200_ok(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["rese"]
        post_api_request_data = request_data["rese"]
        print("make the request")
        post_api_response_data = response_data["rese"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=user_one
        )
        print("verify the response status code")
        assert response.status_code == 201
        print("verify the response data")
        assert response.json() == post_api_response_data

    @pytest.mark.Smoke  # mark the test case as smoke
    def test_reset_post_401_unauthorized(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["rese"]
        post_api_request_data = request_data["rese"]
        print("make the request")
        post_api_response_data = response_data["rese"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=user_one
        )
        print("verify the response status code")
        assert response.status_code == 401
        print("verify the response data")
        assert response.json() == post_api_response_data

    @pytest.mark.Smoke  # mark the test case as smoke
    def test_reset_post_422_data_error(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["rese"]
        post_api_request_data = request_data["rese"]
        print("make the request")
        post_api_response_data = response_data["rese"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=user_one
        )
        print("verify the response status code")
        assert response.status_code == 422
        print("verify the response data")
        assert response.json() == post_api_response_data

    @pytest.mark.Smoke  # mark the test case as smoke
    def test_reset_post_404_not_found(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["rese"]
        post_api_request_data = request_data["rese"]
        print("make the request")
        post_api_response_data = response_data["rese"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=user_one
        )
        print("verify the response status code")
        assert response.status_code == 404
        print("verify the response data")
        assert response.json() == post_api_response_data
