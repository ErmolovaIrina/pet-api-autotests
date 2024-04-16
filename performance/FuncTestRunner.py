import sys
sys.path.append("..")

from locust import HttpUser, task
import json, logging
import lib.config
import lib.utils


class FuncTestRunner(HttpUser):

    def on_start(self):
        # тут мы городим все то что в функциональных тестах делали в conftest
        # тупой логгер
        self.logger = logging.getLogger(__name__)
        # конфиг
        self.configFile = lib.config.Config()
        self.configFile.load("tests_data.yml")
        # утилы
        self.util = lib.utils.Util()
        self.util.init(self.client, self.configFile, self.logger)

    @task(1)
    def perform_request_accounts(self):
        accountTests = Test()
        accountTests.test_post_session(self.client, self.logger, self.configFile, self.util)