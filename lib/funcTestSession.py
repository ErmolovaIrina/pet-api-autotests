import requests, logging, datetime, os
import allure


class FuncTestSession(requests.Session):
    """ подтягиваем к реализацию Session в locust. Там плюс минус все тоже замое за исключением того что юзаются локальные урлы """

    def __init__(self, base_url, logger, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = base_url
        self.logger = logger

    def get(self, url: str, params: dict = None, headers: dict = None, cookies: dict = None, json: dict = None, files: dict = None):
        with allure.step(f"GET to URL '{url}'"):
            return self._send(url, params, headers, cookies, json, files, 'GET')

    def post(self, url: str, params: dict = None, headers: dict = None, cookies: dict = None, json: dict = None, files: dict = None):
        with allure.step(f"POST to URL '{url}'"):
            return self._send(url, params, headers, cookies, json, files, 'POST')

    def put(self, url: str, params: dict = None, headers: dict = None, cookies: dict = None, json: dict = None, files: dict = None):
        with allure.step(f"PUT to URL '{url}'"):
            return self._send(url, params, headers, cookies, json, files, 'PUT')

    def patch(self, url: str, params: dict = None, headers: dict = None, cookies: dict = None, json: dict = None, files: dict = None):
        with allure.step(f"PATCH to URL '{url}'"):
            return self._send(url, params, headers, cookies, json, files, 'PATCH')

    def delete(self, url: str, params: dict = None, headers: dict = None, cookies: dict = None, json: dict = None, files: dict = None):
        with allure.step(f"DELETE to URL '{url}'"):
            return self._send(url, params, headers, cookies, json, files, 'DELETE')

    def _send(self, url: str, data: dict, headers: dict, cookies: dict, json: dict, files: dict, method: str):

        url = f"{self.base_url}{url}"

        if headers is None:
            headers = {}

        if cookies is None:
            cookies = {}

        if json is None:
            json = {}

        if files is None:
            files = {}

        self.format_request(url, data, headers, cookies, json, files, method)

        if method == 'GET':
            response = requests.get(url, params=data, headers=headers, cookies=cookies, json=json, files=files)
        elif method == 'POST':
            response = requests.post(url, params=data, headers=headers, cookies=cookies, json=json, files=files)
        elif method == 'PUT':
            response = requests.put(url, params=data, headers=headers, cookies=cookies, json=json, files=files)
        elif method == 'PATCH':
            response = requests.patch(url, params=data, headers=headers, cookies=cookies, json=json, files=files)
        elif method == 'DELETE':
            response = requests.delete(url, params=data, headers=headers, cookies=cookies, json=json, files=files)
        else:
            raise Exception(f"Bad HTTP method '{method}' was received")

        self.format_response(response)
        return response

    def format_request(self, url: str, data: dict, headers: dict, cookies: dict, json: dict, files: dict, method: str):
        testname = os.environ.get('PYTEST_CURRENT_TEST')

        data_to_add = f"\n-----\n"
        data_to_add += f"Test: {testname}\n"
        data_to_add += f"Time: {str(datetime.datetime.now())}\n"
        data_to_add += f"Request method: {method}\n"
        data_to_add += f"Request URL: {url}\n"
        data_to_add += f"Request data: {data}\n"
        data_to_add += f"Request data: {json}\n"
        data_to_add += f"Request data: {files}\n"
        data_to_add += f"Request headers: {headers}\n"
        data_to_add += f"Request cookies: {cookies}\n"
        data_to_add += "\n"

        self.logger.info(data_to_add)

    def format_response(self, response: requests.Response):
        cookies_as_dict = dict(response.cookies)
        headers_as_dict = dict(response.headers)

        data_to_add = f"Response code: {response.status_code}\n"
        data_to_add += f"Response text: {response.text}\n"
        data_to_add += f"Response headers: {headers_as_dict}\n"
        data_to_add += f"Response cookies: {cookies_as_dict}\n"
        data_to_add += "\n-----\n"

        self.logger.info(data_to_add)