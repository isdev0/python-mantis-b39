import os
import json
import pytest
from fixture.application import Application


fixture = None
config  = None


def load_config(file):
    global config
    if config is None:
        config_json = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        with open(config_json) as f:
            config = json.load(f)
    return config


@pytest.fixture
def app(request):
    global fixture
    browser = request.config.getoption("--browser")
    web_config = load_config(request.config.getoption("--config"))["web"]
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, base_url=web_config["base_url"])
    # fixture.session.do_login(username=web_config["username"], password=web_config["password"])
    return fixture


@pytest.fixture(scope="session", autouse=True)
def terminate(request):
    def fin():
        fixture.session.do_logout()
        fixture.destroy()

    request.addfinalizer(fin)
    return fixture


def pytest_addoption(parser):
    parser.addoption("--browser",  action="store", default="firefox")
    parser.addoption("--config",   action="store", default="config.json")
