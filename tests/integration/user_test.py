import pytest
import requests


class TestAwardMultiEnv:
    @pytest.mark.Regression  # mark the test case as regression
    def test_award_get_200_ok(
        self,
        env_config: dict[str, str],
        header: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        get_api = env_config["awardAPI"]
        get_api_response_data = response_data["awardAPI"]
        # send request
        response = requests.get(host + get_api, headers=header)
        # assert
        assert response.status_code == 200
        assert response.json() == get_api_response_data

    @pytest.mark.Regression  # mark the test case as regression
    def test_award_get_401_unauthorized(
        self,
        env_config: dict[str, str],
        header: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        get_api = env_config["awardAPI"]
        get_api_response_data = response_data["awardAPI"]
        # send request
        response = requests.get(host + get_api, headers=header)
        # assert
        assert response.status_code == 401
        assert response.json() == get_api_response_data

    @pytest.mark.Regression  # mark the test case as regression
    def test_award_get_404_not_found(
        self,
        env_config: dict[str, str],
        header: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        get_api = env_config["awardAPI"]
        get_api_response_data = response_data["awardAPI"]
        # send request
        response = requests.get(host + get_api, headers=header)
        # assert
        assert response.status_code == 404
        assert response.json() == get_api_response_data

    # POST test starts
    @pytest.mark.Smoke  # mark the test case as smoke
    def test_award_post_200_ok(
        self,
        env_config: dict[str, str],
        header: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["awardAPI"]
        post_api_request_data = request_data["awardAPI"]
        print("make the request")
        post_api_response_data = response_data["awardAPI"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=header
        )
        print("verify the response status code")
        assert response.status_code == 201
        print("verify the response data")
        assert response.json() == post_api_response_data

    @pytest.mark.Smoke  # mark the test case as smoke
    def test_award_post_401_unauthorized(
        self,
        env_config: dict[str, str],
        header: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["awardAPI"]
        post_api_request_data = request_data["awardAPI"]
        print("make the request")
        post_api_response_data = response_data["awardAPI"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=header
        )
        print("verify the response status code")
        assert response.status_code == 401
        print("verify the response data")
        assert response.json() == post_api_response_data

    @pytest.mark.Smoke  # mark the test case as smoke
    def test_award_post_422_data_error(
        self,
        env_config: dict[str, str],
        header: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["awardAPI"]
        post_api_request_data = request_data["awardAPI"]
        print("make the request")
        post_api_response_data = response_data["awardAPI"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=header
        )
        print("verify the response status code")
        assert response.status_code == 422
        print("verify the response data")
        assert response.json() == post_api_response_data

    @pytest.mark.Smoke  # mark the test case as smoke
    def test_award_post_404_not_found(
        self,
        env_config: dict[str, str],
        header: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["awardAPI"]
        post_api_request_data = request_data["awardAPI"]
        print("make the request")
        post_api_response_data = response_data["awardAPI"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=header
        )
        print("verify the response status code")
        assert response.status_code == 404
        print("verify the response data")
        assert response.json() == post_api_response_data

    # PUT Test Starts Here
    @pytest.mark.Smoke  # mark the test case as smoke
    def test_award_put_200_ok(
        self,
        env_config: dict[str, str],
        header: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["awardAPI"]
        post_api_request_data = request_data["awardAPI"]
        print("make the request")
        post_api_response_data = response_data["awardAPI"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=header
        )
        print("verify the response status code")
        assert response.status_code == 201
        print("verify the response data")
        assert response.json() == post_api_response_data

    @pytest.mark.Smoke  # mark the test case as smoke
    def test_award_put_401_unauthorized(
        self,
        env_config: dict[str, str],
        header: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["awardAPI"]
        post_api_request_data = request_data["awardAPI"]
        print("make the request")
        post_api_response_data = response_data["awardAPI"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=header
        )
        print("verify the response status code")
        assert response.status_code == 401
        print("verify the response data")
        assert response.json() == post_api_response_data

    @pytest.mark.Smoke  # mark the test case as smoke
    def test_award_put_422_data_error(
        self,
        env_config: dict[str, str],
        header: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["awardAPI"]
        post_api_request_data = request_data["awardAPI"]
        print("make the request")
        post_api_response_data = response_data["awardAPI"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=header
        )
        print("verify the response status code")
        assert response.status_code == 422
        print("verify the response data")
        assert response.json() == post_api_response_data

    @pytest.mark.Smoke  # mark the test case as smoke
    def test_award_put_404_not_found(
        self,
        env_config: dict[str, str],
        header: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["awardAPI"]
        post_api_request_data = request_data["awardAPI"]
        print("make the request")
        post_api_response_data = response_data["awardAPI"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=header
        )
        print("verify the response status code")
        assert response.status_code == 404
        print("verify the response data")
        assert response.json() == post_api_response_data

    # DELETE Starts Here
    @pytest.mark.Regression  # mark the test case as regression
    def test_award_delte_200_ok(
        self,
        env_config: dict[str, str],
        header: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        get_api = env_config["awardAPI"]
        get_api_response_data = response_data["awardAPI"]
        # send request
        response = requests.get(host + get_api, headers=header)
        # assert
        assert response.status_code == 200
        assert response.json() == get_api_response_data

    @pytest.mark.Regression  # mark the test case as regression
    def test_award_delete_401_unauthorized(
        self,
        env_config: dict[str, str],
        header: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        get_api = env_config["awardAPI"]
        get_api_response_data = response_data["awardAPI"]
        # send request
        response = requests.get(host + get_api, headers=header)
        # assert
        assert response.status_code == 401
        assert response.json() == get_api_response_data

    @pytest.mark.Regression  # mark the test case as regression
    def test_award_delete_404_not_found(
        self,
        env_config: dict[str, str],
        header: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        get_api = env_config["awardAPI"]
        get_api_response_data = response_data["awardAPI"]
        # send request
        response = requests.get(host + get_api, headers=header)
        # assert
        assert response.status_code == 404
        assert response.json() == get_api_response_data


# SOCIAL RESTFUL API TEST STARTS HERE
class TestSocialMultiEnv:
    @pytest.mark.Regression  # mark the test case as regression
    def test_social_get_200_ok(
        self,
        env_config: dict[str, str],
        header: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        get_api = env_config["socialAPI"]
        get_api_response_data = response_data["socialAPI"]
        # send request
        response = requests.get(host + get_api, headers=header)
        # assert
        assert response.status_code == 200
        assert response.json() == get_api_response_data

    @pytest.mark.Regression  # mark the test case as regression
    def test_social_get_401_unauthorized(
        self,
        env_config: dict[str, str],
        header: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        get_api = env_config["socialAPI"]
        get_api_response_data = response_data["socialAPI"]
        # send request
        response = requests.get(host + get_api, headers=header)
        # assert
        assert response.status_code == 401
        assert response.json() == get_api_response_data

    @pytest.mark.Regression  # mark the test case as regression
    def test_social_get_404_not_found(
        self,
        env_config: dict[str, str],
        header: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        get_api = env_config["socialAPI"]
        get_api_response_data = response_data["socialAPI"]
        # send request
        response = requests.get(host + get_api, headers=header)
        # assert
        assert response.status_code == 404
        assert response.json() == get_api_response_data

    # POST test starts
    @pytest.mark.Smoke  # mark the test case as smoke
    def test_social_post_200_ok(
        self,
        env_config: dict[str, str],
        header: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["socialAPI"]
        post_api_request_data = request_data["socialAPI"]
        print("make the request")
        post_api_response_data = response_data["socialAPI"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=header
        )
        print("verify the response status code")
        assert response.status_code == 201
        print("verify the response data")
        assert response.json() == post_api_response_data

    @pytest.mark.Smoke  # mark the test case as smoke
    def test_social_post_401_unauthorized(
        self,
        env_config: dict[str, str],
        header: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["socialAPI"]
        post_api_request_data = request_data["socialAPI"]
        print("make the request")
        post_api_response_data = response_data["socialAPI"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=header
        )
        print("verify the response status code")
        assert response.status_code == 401
        print("verify the response data")
        assert response.json() == post_api_response_data

    @pytest.mark.Smoke  # mark the test case as smoke
    def test_social_post_422_data_error(
        self,
        env_config: dict[str, str],
        header: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["socialAPI"]
        post_api_request_data = request_data["socialAPI"]
        print("make the request")
        post_api_response_data = response_data["socialAPI"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=header
        )
        print("verify the response status code")
        assert response.status_code == 422
        print("verify the response data")
        assert response.json() == post_api_response_data

    @pytest.mark.Smoke  # mark the test case as smoke
    def test_social_post_404_not_found(
        self,
        env_config: dict[str, str],
        header: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["socialAPI"]
        post_api_request_data = request_data["socialAPI"]
        print("make the request")
        post_api_response_data = response_data["socialAPI"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=header
        )
        print("verify the response status code")
        assert response.status_code == 404
        print("verify the response data")
        assert response.json() == post_api_response_data

    # PUT Test Starts Here
    @pytest.mark.Smoke  # mark the test case as smoke
    def test_social_put_200_ok(
        self,
        env_config: dict[str, str],
        header: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["socialAPI"]
        post_api_request_data = request_data["socialAPI"]
        print("make the request")
        post_api_response_data = response_data["socialAPI"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=header
        )
        print("verify the response status code")
        assert response.status_code == 201
        print("verify the response data")
        assert response.json() == post_api_response_data

    @pytest.mark.Smoke  # mark the test case as smoke
    def test_social_put_401_unauthorized(
        self,
        env_config: dict[str, str],
        header: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["socialAPI"]
        post_api_request_data = request_data["socialAPI"]
        print("make the request")
        post_api_response_data = response_data["socialAPI"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=header
        )
        print("verify the response status code")
        assert response.status_code == 401
        print("verify the response data")
        assert response.json() == post_api_response_data

    @pytest.mark.Smoke  # mark the test case as smoke
    def test_social_put_422_data_error(
        self,
        env_config: dict[str, str],
        header: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["socialAPI"]
        post_api_request_data = request_data["socialAPI"]
        print("make the request")
        post_api_response_data = response_data["socialAPI"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=header
        )
        print("verify the response status code")
        assert response.status_code == 422
        print("verify the response data")
        assert response.json() == post_api_response_data

    @pytest.mark.Smoke  # mark the test case as smoke
    def test_social_put_404_not_found(
        self,
        env_config: dict[str, str],
        header: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["socialAPI"]
        post_api_request_data = request_data["socialAPI"]
        print("make the request")
        post_api_response_data = response_data["socialAPI"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=header
        )
        print("verify the response status code")
        assert response.status_code == 404
        print("verify the response data")
        assert response.json() == post_api_response_data

    # DELETE Starts Here
    @pytest.mark.Regression  # mark the test case as regression
    def test_social_delte_200_ok(
        self,
        env_config: dict[str, str],
        header: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        get_api = env_config["socialAPI"]
        get_api_response_data = response_data["socialAPI"]
        # send request
        response = requests.get(host + get_api, headers=header)
        # assert
        assert response.status_code == 200
        assert response.json() == get_api_response_data

    @pytest.mark.Regression  # mark the test case as regression
    def test_social_delete_401_unauthorized(
        self,
        env_config: dict[str, str],
        header: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        get_api = env_config["socialAPI"]
        get_api_response_data = response_data["socialAPI"]
        # send request
        response = requests.get(host + get_api, headers=header)
        # assert
        assert response.status_code == 401
        assert response.json() == get_api_response_data

    @pytest.mark.Regression  # mark the test case as regression
    def test_social_delete_404_not_found(
        self,
        env_config: dict[str, str],
        header: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        get_api = env_config["socialAPI"]
        get_api_response_data = response_data["socialAPI"]
        # send request
        response = requests.get(host + get_api, headers=header)
        # assert
        assert response.status_code == 404
        assert response.json() == get_api_response_data


# PROFILE RESTFUL API TEST STARTS HERE
class TestprofileMultiEnv:
    @pytest.mark.Regression  # mark the test case as regression
    def test_profile_get_200_ok(
        self,
        env_config: dict[str, str],
        header: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        get_api = env_config["profileAPI"]
        get_api_response_data = response_data["profileAPI"]
        # send request
        response = requests.get(host + get_api, headers=header)
        # assert
        assert response.status_code == 200
        assert response.json() == get_api_response_data

    @pytest.mark.Regression  # mark the test case as regression
    def test_profile_get_401_unauthorized(
        self,
        env_config: dict[str, str],
        header: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        get_api = env_config["profileAPI"]
        get_api_response_data = response_data["profileAPI"]
        # send request
        response = requests.get(host + get_api, headers=header)
        # assert
        assert response.status_code == 401
        assert response.json() == get_api_response_data

    @pytest.mark.Regression  # mark the test case as regression
    def test_profile_get_404_not_found(
        self,
        env_config: dict[str, str],
        header: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        get_api = env_config["profileAPI"]
        get_api_response_data = response_data["profileAPI"]
        # send request
        response = requests.get(host + get_api, headers=header)
        # assert
        assert response.status_code == 404
        assert response.json() == get_api_response_data

    # POST test starts
    @pytest.mark.Smoke  # mark the test case as smoke
    def test_profile_post_200_ok(
        self,
        env_config: dict[str, str],
        header: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["profileAPI"]
        post_api_request_data = request_data["profileAPI"]
        print("make the request")
        post_api_response_data = response_data["profileAPI"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=header
        )
        print("verify the response status code")
        assert response.status_code == 201
        print("verify the response data")
        assert response.json() == post_api_response_data

    @pytest.mark.Smoke  # mark the test case as smoke
    def test_profile_post_401_unauthorized(
        self,
        env_config: dict[str, str],
        header: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        post_api = env_config["profileAPI"]
        post_api_request_data = request_data["profileAPI"]
        print("make the request")
        post_api_response_data = response_data["profileAPI"]
        # Your test code here
        response = requests.post(
            host + post_api, json=post_api_request_data, headers=header
        )
        print("verify the response status code")
        assert response.status_code == 401
        print("verify the response data")
        assert response.json() == post_api_response_data

    # DELETE Starts Here
    @pytest.mark.Regression  # mark the test case as regression
    def test_profile_delte_200_ok(
        self,
        env_config: dict[str, str],
        header: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        get_api = env_config["profileAPI"]
        get_api_response_data = response_data["profileAPI"]
        # send request
        response = requests.get(host + get_api, headers=header)
        # assert
        assert response.status_code == 200
        assert response.json() == get_api_response_data

    @pytest.mark.Regression  # mark the test case as regression
    def test_profile_delete_401_unauthorized(
        self,
        env_config: dict[str, str],
        header: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        get_api = env_config["profileAPI"]
        get_api_response_data = response_data["profileAPI"]
        # send request
        response = requests.get(host + get_api, headers=header)
        # assert
        assert response.status_code == 401
        assert response.json() == get_api_response_data

    @pytest.mark.Regression  # mark the test case as regression
    def test_profile_delete_404_not_found(
        self,
        env_config: dict[str, str],
        header: dict[str, str],
        request_data: dict[str, str],
        response_data: dict[str, str],
    ) -> None:
        host = env_config["host"]
        get_api = env_config["profileAPI"]
        get_api_response_data = response_data["profileAPI"]
        # send request
        response = requests.get(host + get_api, headers=header)
        # assert
        assert response.status_code == 404
        assert response.json() == get_api_response_data
