from requests import Response
import json

class Assertions:
    @staticmethod
    def assert_code_status(response: Response, expected_status_code):
        assert response.status_code == expected_status_code, \
            f"Unexpected status code! Expected: {expected_status_code} Actual: {response.status_code}"

    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value, error_message ):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        assert name in response_as_dict, f"Response JSON doesn't have key '{name}'"
        assert response_as_dict[name] == expected_value, error_message

    @staticmethod
    def assert_header(response: Response, headers_name, value):
        try:
            headers = response.headers
        except:
            assert False, f"No one hearers in response."

        assert headers[headers_name] == value, f"There is no this value in headers"


    @staticmethod
    def assert_invalid_request_message(response: Response, expected_message):
        assert response.json()["message"] == f"{expected_message}", f"response has other message, '{response.content}'"


    @staticmethod
    def assert_response_message(response: Response, key, expected_message):
        assert response.json()[key] == f"{expected_message}", f"response has other message, '{response.content}'"

    @staticmethod
    def assert_json_has_key(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        assert name in response_as_dict, f"Response JSON doesn't have key '{name}'"

    @staticmethod
    def assert_json_has_keys(response: Response, names: list):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        for name in names:
            assert name in response_as_dict, f"Response JSON doesn't have key '{name}'"
    @staticmethod
    def assert_json_has_keys_in_dict(response: Response, names: list):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        for name in names:
            assert name in response_as_dict[0], f"Response JSON doesn't have key '{name}'"
    @staticmethod
    def assert_json_has_keys_in_json_item(item: dict, names: list):

        for name in names:
            assert name in item, f"Response JSON doesn't have key '{name}'"
    @staticmethod
    def assert_json_has_not_key(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        assert name not in response_as_dict, f"Response JSON shouldn't have key '{name}', but it's present"

    @staticmethod
    def assert_json_has_not_keys(response: Response, names: list):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        for name in names:
            assert name not in response_as_dict, f"Response JSON shouldn't have key '{name}', but it's present'"

    @staticmethod
    def assert_bad_request(response: Response, item: dict, field, message):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        # проверяем что в основном ответе есть стандартная структура
        names = ["status", "description", "message", "errors"]
        for name in names:
            assert name in response_as_dict, f"Response is not in JSON format. Response text is '{response.text}'"

        # проверяем ошибочные поля в структуре ответа
        errorItem = f"{response_as_dict}{item}"

        assert errorItem == field, f"Incorrect field has other value. Correct field is '{response_as_dict}'"
        assert errorItem == message, f"Incorrect message has other text. Correct message is '{response_as_dict}'"

    @staticmethod
    def assert_json_has_correct_value_in_key(response: Response, objectName, keyName, badValues: list):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"
        badValues = badValues
        for e in response_as_dict[f"{objectName}"]:
            assert e[f'{keyName}'] not in badValues, f"Response has bad value in key {keyName}"
    @staticmethod
    def assert_erorrs_4xx(response: Response, errorMessage: str, message: str, statusCode):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        names = ["status", "description", "message", "errors"]
        #проверяем структуру
        for name in names:
            assert name in response_as_dict, f"There is no structure key in response. Actual is {response.text}"

        # проверяем текст сообщения в основном блоке
        assert response_as_dict["message"] == errorMessage, f"There is other status code in response structure"
        # проверяем что статус соответствует коду ответа
        assert response_as_dict["status"] == statusCode, f"There is other status code in response structure"
        # проверяем текст сообщения в блоке ерроров
        assert response_as_dict["errors"][0]["message"] == message, f"There is other text in response. Actual is {response.text}"

    @staticmethod
    def assert_match_code_and_message(response: Response, message: str, code):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"
        # проверяем что статус соответствует коду ответа

        assert response_as_dict["errors"][0]["code"] == code, f"There is other status code in response structure"
        # проверяем текст сообщения
        assert response_as_dict["errors"][0]["message"] == message, f"There is other text in response. Actual is {response.text}"

    @staticmethod
    def assert_find_keys_name(response: Response, pattern: str, number: int, keys: list):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not in JSON Format. Response text is '{response.text}'"

        for i in response_as_dict:
            if i[::number] == pattern:
                for k in keys:
                    assert k in response_as_dict, f"Couldn't find these keys in response model. Response is {response_as_dict}"
            else: print("This object doesn't have these keys")






