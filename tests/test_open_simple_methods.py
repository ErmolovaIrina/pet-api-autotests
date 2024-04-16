import allure, pytest
from lib.assertions import Assertions
from lib.utils import Util

@allure.epic("Простые методы")
class TestSimpleMethod():

  # /api/hello

    @allure.title("Get hello")
    def test_get_hello(self, init_http_session,init_logger, init_config, init_util):
        params = {"name": "Irina"}
        response = init_http_session.get("/api/hello", params=params)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "answer")
        Assertions.assert_response_message(response, "answer", "Hello, Irina")

    @allure.title("Get hello without params")
    def test_get_hello_no_params(self, init_http_session,init_logger, init_config, init_util):
        response = init_http_session.post("/api/hello")

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "answer")
        Assertions.assert_response_message(response, "answer", "Hello, someone")

    @allure.title("Get hello wrong method")
    def test_wrong_method_hello(self, init_http_session,init_logger, init_config, init_util):
        params = {"name": "Irina"}
        response = init_http_session.post("/api/hello", params=params)

        Assertions.assert_code_status(response, 415)

  # /api/check_type

    @allure.title("Check GET request")
    def test_get_check_type(self, init_http_session,init_logger, init_config, init_util):
        response = init_http_session.get("/api/check_type")
        Assertions.assert_code_status(response, 200)


    @allure.title("Check POST request")
    def test_post_check_type(self, init_http_session,init_logger, init_config, init_util):
        response = init_http_session.post("/api/check_type")
        Assertions.assert_code_status(response, 200)

# get_json

    @allure.title("Check get_json")
    def test_get_json(self, init_http_session,init_logger, init_config, init_util):
        response = init_http_session.get("api/get_json")
        Assertions.assert_code_status(response, 200)
        keys = ["name", "fname"]
        Assertions.assert_json_has_keys(response, keys)

