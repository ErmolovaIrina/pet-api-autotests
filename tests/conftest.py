import pytest, requests, logging, datetime, allure

import lib.funcTestSession
import lib.config
import lib.utils

logger  = None
configFile = None
util = None

@allure.title("Подготовка сессии")
@pytest.fixture()
def init_http_session():
    # возвращаем экземпляр реквеста который мы будем использовать далее
    global logger
    global configFile
    return lib.funcTestSession.FuncTestSession(configFile.base_url, logger)

@allure.title("Доступ к классу утилов")
@pytest.fixture()
def init_util():
    return util

@allure.title("Логирование")
@pytest.fixture()
def init_logger():
    return logger

@allure.title("Конфиг с данными")
@pytest.fixture()
def init_config():
    return configFile

@allure.title("Старт сессии")
def pytest_sessionstart(session):
    # настраиваем логгер
    global logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s %(levelname)s line:%(lineno)s  %(message)s', datefmt="%H:%M:%S")

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)

    filehandler = logging.FileHandler(
        r'./logs/logger-{}.txt'.format(format(datetime.datetime.strftime(datetime.date.today(), r'%Y-%m-%dT%H:%M'))))
    filehandler.setLevel(logging.INFO)
    filehandler.setFormatter(formatter)

    errorhandler = logging.FileHandler(
        r'./logs/\error\error-{}.txt'.format(format(datetime.datetime.strftime(datetime.date.today(), r'%Y-%m-%dT%H:%M'))))
    errorhandler.setLevel(logging.ERROR)
    errorhandler.setFormatter(formatter)

    # logger.addHandler(console)
    logger.addHandler(filehandler)
    logger.addHandler(errorhandler)

    logger.info("loggers initialized")

    # конфиг
    global configFile
    configFile = lib.config.Config()
    configFile.load("tests_data.yml")

    # промежуточный класс со всяким разным
    global util
    util = lib.utils.Util()
    util.init(lib.funcTestSession.FuncTestSession(configFile.base_url, logger), configFile, logger)
