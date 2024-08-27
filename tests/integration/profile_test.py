import pytest
import requests


class TestBaseMultiEnv:
    @pytest.mark.Regression  # mark the test case as regression
    def test_base_get_200_ok(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        get_api = env_config["baseAPI"]
        get_api_response_data = response_data["baseAPI"]
        # send request
        response = requests.get(host + get_api, headers=user_one)
        # assert
        assert response.status_code == 200
        assert response.json() == get_api_response_data

    @pytest.mark.Regression  # mark the test case as regression
    def test_base_get_401_unauthorized(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        get_api = env_config["baseAPI"]
        get_api_response_data = response_data["baseAPI"]
        # send request
        response = requests.get(host + get_api, headers=user_one)
        # assert
        assert response.status_code == 401
        assert response.json() == get_api_response_data

    @pytest.mark.Regression  # mark the test case as regression
    def test_base_get_404_not_found(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        get_api = env_config["baseAPI"]
        get_api_response_data = response_data["baseAPI"]
        # send request
        response = requests.get(host + get_api, headers=user_one)
        # assert
        assert response.status_code == 404
        assert response.json() == get_api_response_data

    # POST test starts
    @pytest.mark.Smoke  # mark the test case as smoke
    def test_base_post_200_ok(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["baseAPI"]
        post_api_request_data = request_data["baseAPI"]
        print("make the request")
        post_api_response_data = response_data["baseAPI"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=user_one
        )
        print("verify the response status code")
        assert response.status_code == 201
        print("verify the response data")
        assert response.json() == post_api_response_data

    @pytest.mark.Smoke  # mark the test case as smoke
    def test_base_post_401_unauthorized(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["baseAPI"]
        post_api_request_data = request_data["baseAPI"]
        print("make the request")
        post_api_response_data = response_data["baseAPI"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=user_one
        )
        print("verify the response status code")
        assert response.status_code == 401
        print("verify the response data")
        assert response.json() == post_api_response_data

    @pytest.mark.Smoke  # mark the test case as smoke
    def test_base_post_422_data_error(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["baseAPI"]
        post_api_request_data = request_data["baseAPI"]
        print("make the request")
        post_api_response_data = response_data["baseAPI"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=user_one
        )
        print("verify the response status code")
        assert response.status_code == 422
        print("verify the response data")
        assert response.json() == post_api_response_data

    @pytest.mark.Smoke  # mark the test case as smoke
    def test_base_post_404_not_found(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["baseAPI"]
        post_api_request_data = request_data["baseAPI"]
        print("make the request")
        post_api_response_data = response_data["baseAPI"]
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
    def test_base_put_200_ok(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["baseAPI"]
        post_api_request_data = request_data["baseAPI"]
        print("make the request")
        post_api_response_data = response_data["baseAPI"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=user_one
        )
        print("verify the response status code")
        assert response.status_code == 201
        print("verify the response data")
        assert response.json() == post_api_response_data

    @pytest.mark.Smoke  # mark the test case as smoke
    def test_base_put_401_unauthorized(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["baseAPI"]
        post_api_request_data = request_data["baseAPI"]
        print("make the request")
        post_api_response_data = response_data["baseAPI"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=user_one
        )
        print("verify the response status code")
        assert response.status_code == 401
        print("verify the response data")
        assert response.json() == post_api_response_data

    @pytest.mark.Smoke  # mark the test case as smoke
    def test_base_put_422_data_error(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["baseAPI"]
        post_api_request_data = request_data["baseAPI"]
        print("make the request")
        post_api_response_data = response_data["baseAPI"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=user_one
        )
        print("verify the response status code")
        assert response.status_code == 422
        print("verify the response data")
        assert response.json() == post_api_response_data

    @pytest.mark.Smoke  # mark the test case as smoke
    def test_base_put_404_not_found(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["baseAPI"]
        post_api_request_data = request_data["baseAPI"]
        print("make the request")
        post_api_response_data = response_data["baseAPI"]
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
    def test_base_delte_200_ok(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        get_api = env_config["baseAPI"]
        get_api_response_data = response_data["baseAPI"]
        # send request
        response = requests.get(host + get_api, headers=user_one)
        # assert
        assert response.status_code == 200
        assert response.json() == get_api_response_data

    @pytest.mark.Regression  # mark the test case as regression
    def test_base_delete_401_unauthorized(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        get_api = env_config["baseAPI"]
        get_api_response_data = response_data["baseAPI"]
        # send request
        response = requests.get(host + get_api, headers=user_one)
        # assert
        assert response.status_code == 401
        assert response.json() == get_api_response_data

    @pytest.mark.Regression  # mark the test case as regression
    def test_base_delete_404_not_found(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        get_api = env_config["baseAPI"]
        get_api_response_data = response_data["baseAPI"]
        # send request
        response = requests.get(host + get_api, headers=user_one)
        # assert
        assert response.status_code == 404
        assert response.json() == get_api_response_data


# ACCADEMICS RESTFUL API TEST STARTS HERE
class TestAccademicsMultiEnv:
    @pytest.mark.Regression  # mark the test case as regression
    def test_accademics_get_200_ok(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        get_api = env_config["accademicsAPI"]
        get_api_response_data = response_data["accademicsAPI"]
        # send request
        response = requests.get(host + get_api, headers=user_one)
        # assert
        assert response.status_code == 200
        assert response.json() == get_api_response_data

    @pytest.mark.Regression  # mark the test case as regression
    def test_accademics_get_401_unauthorized(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        get_api = env_config["accademicsAPI"]
        get_api_response_data = response_data["accademicsAPI"]
        # send request
        response = requests.get(host + get_api, headers=user_one)
        # assert
        assert response.status_code == 401
        assert response.json() == get_api_response_data

    @pytest.mark.Regression  # mark the test case as regression
    def test_accademics_get_404_not_found(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        get_api = env_config["accademicsAPI"]
        get_api_response_data = response_data["accademicsAPI"]
        # send request
        response = requests.get(host + get_api, headers=user_one)
        # assert
        assert response.status_code == 404
        assert response.json() == get_api_response_data

    # POST test starts
    @pytest.mark.Smoke  # mark the test case as smoke
    def test_accademics_post_200_ok(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["accademicsAPI"]
        post_api_request_data = request_data["accademicsAPI"]
        print("make the request")
        post_api_response_data = response_data["accademicsAPI"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=user_one
        )
        print("verify the response status code")
        assert response.status_code == 201
        print("verify the response data")
        assert response.json() == post_api_response_data

    @pytest.mark.Smoke  # mark the test case as smoke
    def test_accademics_post_401_unauthorized(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["accademicsAPI"]
        post_api_request_data = request_data["accademicsAPI"]
        print("make the request")
        post_api_response_data = response_data["accademicsAPI"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=user_one
        )
        print("verify the response status code")
        assert response.status_code == 401
        print("verify the response data")
        assert response.json() == post_api_response_data

    @pytest.mark.Smoke  # mark the test case as smoke
    def test_accademics_post_422_data_error(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["accademicsAPI"]
        post_api_request_data = request_data["accademicsAPI"]
        print("make the request")
        post_api_response_data = response_data["accademicsAPI"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=user_one
        )
        print("verify the response status code")
        assert response.status_code == 422
        print("verify the response data")
        assert response.json() == post_api_response_data

    @pytest.mark.Smoke  # mark the test case as smoke
    def test_accademics_post_404_not_found(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["accademicsAPI"]
        post_api_request_data = request_data["accademicsAPI"]
        print("make the request")
        post_api_response_data = response_data["accademicsAPI"]
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
    def test_accademics_put_200_ok(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["accademicsAPI"]
        post_api_request_data = request_data["accademicsAPI"]
        print("make the request")
        post_api_response_data = response_data["accademicsAPI"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=user_one
        )
        print("verify the response status code")
        assert response.status_code == 201
        print("verify the response data")
        assert response.json() == post_api_response_data

    @pytest.mark.Smoke  # mark the test case as smoke
    def test_accademics_put_401_unauthorized(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["accademicsAPI"]
        post_api_request_data = request_data["accademicsAPI"]
        print("make the request")
        post_api_response_data = response_data["accademicsAPI"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=user_one
        )
        print("verify the response status code")
        assert response.status_code == 401
        print("verify the response data")
        assert response.json() == post_api_response_data

    @pytest.mark.Smoke  # mark the test case as smoke
    def test_accademics_put_422_data_error(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["accademicsAPI"]
        post_api_request_data = request_data["accademicsAPI"]
        print("make the request")
        post_api_response_data = response_data["accademicsAPI"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=user_one
        )
        print("verify the response status code")
        assert response.status_code == 422
        print("verify the response data")
        assert response.json() == post_api_response_data

    @pytest.mark.Smoke  # mark the test case as smoke
    def test_accademics_put_404_not_found(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["accademicsAPI"]
        post_api_request_data = request_data["accademicsAPI"]
        print("make the request")
        post_api_response_data = response_data["accademicsAPI"]
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
    def test_accademics_delte_200_ok(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        get_api = env_config["accademicsAPI"]
        get_api_response_data = response_data["accademicsAPI"]
        # send request
        response = requests.get(host + get_api, headers=user_one)
        # assert
        assert response.status_code == 200
        assert response.json() == get_api_response_data

    @pytest.mark.Regression  # mark the test case as regression
    def test_accademics_delete_401_unauthorized(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        get_api = env_config["accademicsAPI"]
        get_api_response_data = response_data["accademicsAPI"]
        # send request
        response = requests.get(host + get_api, headers=user_one)
        # assert
        assert response.status_code == 401
        assert response.json() == get_api_response_data

    @pytest.mark.Regression  # mark the test case as regression
    def test_accademics_delete_404_not_found(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        get_api = env_config["accademicsAPI"]
        get_api_response_data = response_data["accademicsAPI"]
        # send request
        response = requests.get(host + get_api, headers=user_one)
        # assert
        assert response.status_code == 404
        assert response.json() == get_api_response_data


# RESEARCH RESTFUL API TEST STARTS HERE
class TestResearcherMultiEnv:
    @pytest.mark.Regression  # mark the test case as regression
    def test_researcher_get_200_ok(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        get_api = env_config["researcherAPI"]
        get_api_response_data = response_data["researcherAPI"]
        # send request
        response = requests.get(host + get_api, headers=user_one)
        # assert
        assert response.status_code == 200
        assert response.json() == get_api_response_data

    @pytest.mark.Regression  # mark the test case as regression
    def test_researcher_get_401_unauthorized(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        get_api = env_config["researcherAPI"]
        get_api_response_data = response_data["researcherAPI"]
        # send request
        response = requests.get(host + get_api, headers=user_one)
        # assert
        assert response.status_code == 401
        assert response.json() == get_api_response_data

    @pytest.mark.Regression  # mark the test case as regression
    def test_researcher_get_404_not_found(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        get_api = env_config["researcherAPI"]
        get_api_response_data = response_data["researcherAPI"]
        # send request
        response = requests.get(host + get_api, headers=user_one)
        # assert
        assert response.status_code == 404
        assert response.json() == get_api_response_data

    # POST test starts
    @pytest.mark.Smoke  # mark the test case as smoke
    def test_researcher_post_200_ok(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["researcherAPI"]
        post_api_request_data = request_data["researcherAPI"]
        print("make the request")
        post_api_response_data = response_data["researcherAPI"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=user_one
        )
        print("verify the response status code")
        assert response.status_code == 201
        print("verify the response data")
        assert response.json() == post_api_response_data

    @pytest.mark.Smoke  # mark the test case as smoke
    def test_researcher_post_401_unauthorized(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["researcherAPI"]
        post_api_request_data = request_data["researcherAPI"]
        print("make the request")
        post_api_response_data = response_data["researcherAPI"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=user_one
        )
        print("verify the response status code")
        assert response.status_code == 401
        print("verify the response data")
        assert response.json() == post_api_response_data

    @pytest.mark.Smoke  # mark the test case as smoke
    def test_researcher_post_422_data_error(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["researcherAPI"]
        post_api_request_data = request_data["researcherAPI"]
        print("make the request")
        post_api_response_data = response_data["researcherAPI"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=user_one
        )
        print("verify the response status code")
        assert response.status_code == 422
        print("verify the response data")
        assert response.json() == post_api_response_data

    @pytest.mark.Smoke  # mark the test case as smoke
    def test_researcher_post_404_not_found(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["researcherAPI"]
        post_api_request_data = request_data["researcherAPI"]
        print("make the request")
        post_api_response_data = response_data["researcherAPI"]
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
    def test_researcher_put_200_ok(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["researcherAPI"]
        post_api_request_data = request_data["researcherAPI"]
        print("make the request")
        post_api_response_data = response_data["researcherAPI"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=user_one
        )
        print("verify the response status code")
        assert response.status_code == 201
        print("verify the response data")
        assert response.json() == post_api_response_data

    @pytest.mark.Smoke  # mark the test case as smoke
    def test_researcher_put_401_unauthorized(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["researcherAPI"]
        post_api_request_data = request_data["researcherAPI"]
        print("make the request")
        post_api_response_data = response_data["researcherAPI"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=user_one
        )
        print("verify the response status code")
        assert response.status_code == 401
        print("verify the response data")
        assert response.json() == post_api_response_data

    @pytest.mark.Smoke  # mark the test case as smoke
    def test_researcher_put_422_data_error(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["researcherAPI"]
        post_api_request_data = request_data["researcherAPI"]
        print("make the request")
        post_api_response_data = response_data["researcherAPI"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=user_one
        )
        print("verify the response status code")
        assert response.status_code == 422
        print("verify the response data")
        assert response.json() == post_api_response_data

    @pytest.mark.Smoke  # mark the test case as smoke
    def test_researcher_put_404_not_found(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["researcherAPI"]
        post_api_request_data = request_data["researcherAPI"]
        print("make the request")
        post_api_response_data = response_data["researcherAPI"]
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
    def test_researcher_delte_200_ok(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        get_api = env_config["researcherAPI"]
        get_api_response_data = response_data["researcherAPI"]
        # send request
        response = requests.get(host + get_api, headers=user_one)
        # assert
        assert response.status_code == 200
        assert response.json() == get_api_response_data

    @pytest.mark.Regression  # mark the test case as regression
    def test_researcher_delete_401_unauthorized(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        get_api = env_config["researcherAPI"]
        get_api_response_data = response_data["researcherAPI"]
        # send request
        response = requests.get(host + get_api, headers=user_one)
        # assert
        assert response.status_code == 401
        assert response.json() == get_api_response_data

    @pytest.mark.Regression  # mark the test case as regression
    def test_researcher_delete_404_not_found(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        get_api = env_config["researcherAPI"]
        get_api_response_data = response_data["researcherAPI"]
        # send request
        response = requests.get(host + get_api, headers=user_one)
        # assert
        assert response.status_code == 404
        assert response.json() == get_api_response_data


# WORK RESTFUL API TEST STARTS HERE
class TestWorkMultiEnv:
    @pytest.mark.Regression  # mark the test case as regression
    def test_work_get_200_ok(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        get_api = env_config["workAPI"]
        get_api_response_data = response_data["workAPI"]
        # send request
        response = requests.get(host + get_api, headers=user_one)
        # assert
        assert response.status_code == 200
        assert response.json() == get_api_response_data

    @pytest.mark.Regression  # mark the test case as regression
    def test_work_get_401_unauthorized(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        get_api = env_config["workAPI"]
        get_api_response_data = response_data["workAPI"]
        # send request
        response = requests.get(host + get_api, headers=user_one)
        # assert
        assert response.status_code == 401
        assert response.json() == get_api_response_data

    @pytest.mark.Regression  # mark the test case as regression
    def test_work_get_404_not_found(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        get_api = env_config["workAPI"]
        get_api_response_data = response_data["workAPI"]
        # send request
        response = requests.get(host + get_api, headers=user_one)
        # assert
        assert response.status_code == 404
        assert response.json() == get_api_response_data

    # POST test starts
    @pytest.mark.Smoke  # mark the test case as smoke
    def test_work_post_200_ok(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["workAPI"]
        post_api_request_data = request_data["workAPI"]
        print("make the request")
        post_api_response_data = response_data["workAPI"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=user_one
        )
        print("verify the response status code")
        assert response.status_code == 201
        print("verify the response data")
        assert response.json() == post_api_response_data

    @pytest.mark.Smoke  # mark the test case as smoke
    def test_work_post_401_unauthorized(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["workAPI"]
        post_api_request_data = request_data["workAPI"]
        print("make the request")
        post_api_response_data = response_data["workAPI"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=user_one
        )
        print("verify the response status code")
        assert response.status_code == 401
        print("verify the response data")
        assert response.json() == post_api_response_data

    @pytest.mark.Smoke  # mark the test case as smoke
    def test_work_post_422_data_error(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["workAPI"]
        post_api_request_data = request_data["workAPI"]
        print("make the request")
        post_api_response_data = response_data["workAPI"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=user_one
        )
        print("verify the response status code")
        assert response.status_code == 422
        print("verify the response data")
        assert response.json() == post_api_response_data

    @pytest.mark.Smoke  # mark the test case as smoke
    def test_work_post_404_not_found(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["workAPI"]
        post_api_request_data = request_data["workAPI"]
        print("make the request")
        post_api_response_data = response_data["workAPI"]
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
    def test_work_put_200_ok(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["workAPI"]
        post_api_request_data = request_data["workAPI"]
        print("make the request")
        post_api_response_data = response_data["workAPI"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=user_one
        )
        print("verify the response status code")
        assert response.status_code == 201
        print("verify the response data")
        assert response.json() == post_api_response_data

    @pytest.mark.Smoke  # mark the test case as smoke
    def test_work_put_401_unauthorized(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["workAPI"]
        post_api_request_data = request_data["workAPI"]
        print("make the request")
        post_api_response_data = response_data["workAPI"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=user_one
        )
        print("verify the response status code")
        assert response.status_code == 401
        print("verify the response data")
        assert response.json() == post_api_response_data

    @pytest.mark.Smoke  # mark the test case as smoke
    def test_work_put_422_data_error(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["workAPI"]
        post_api_request_data = request_data["workAPI"]
        print("make the request")
        post_api_response_data = response_data["workAPI"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=user_one
        )
        print("verify the response status code")
        assert response.status_code == 422
        print("verify the response data")
        assert response.json() == post_api_response_data

    @pytest.mark.Smoke  # mark the test case as smoke
    def test_work_put_404_not_found(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["workAPI"]
        post_api_request_data = request_data["workAPI"]
        print("make the request")
        post_api_response_data = response_data["workAPI"]
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
    def test_work_delte_200_ok(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        get_api = env_config["workAPI"]
        get_api_response_data = response_data["workAPI"]
        # send request
        response = requests.get(host + get_api, headers=user_one)
        # assert
        assert response.status_code == 200
        assert response.json() == get_api_response_data

    @pytest.mark.Regression  # mark the test case as regression
    def test_work_delete_401_unauthorized(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        get_api = env_config["workAPI"]
        get_api_response_data = response_data["workAPI"]
        # send request
        response = requests.get(host + get_api, headers=user_one)
        # assert
        assert response.status_code == 401
        assert response.json() == get_api_response_data

    @pytest.mark.Regression  # mark the test case as regression
    def test_work_delete_404_not_found(
        self,
        env_config: dict[str, str],
        user_one: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        get_api = env_config["workAPI"]
        get_api_response_data = response_data["workAPI"]
        # send request
        response = requests.get(host + get_api, headers=user_one)
        # assert
        assert response.status_code == 404
        assert response.json() == get_api_response_data
