import importlib
import os
import json
import pytest
import ftputil
from fixture.application import Application
from fixture.db import DbFixture


fixture = None
config = None


def load_config(file):
    global config
    if config is None:
        config_json = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        with open(config_json) as f:
            config = json.load(f)
    return config


@pytest.fixture(scope="session")
def conf(request):
    return load_config(request.config.getoption("--config"))


@pytest.fixture
def app(request, conf):
    global fixture
    browser = request.config.getoption("--browser")
    web_config = config["web"]
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, config=config)
    # fixture.session.do_login(username=web_config["username"], password=web_config["password"])
    return fixture


def replace_server_config(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile("config_inc.php.def"):
            remote.remove("config_inc.php.def")
        if remote.path.isfile("config_inc.php"):
            remote.rename("config_inc.php", "config_inc.php.def")
        remote.upload(os.path.join(os.path.dirname(__file__), "resources/config_inc.php"), "config_inc.php")


def restore_server_config(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile("config_inc.php.def"):
            if remote.path.isfile("config_inc.php"):
                remote.remove("config_inc.php")
            remote.rename("config_inc.php.def", "config_inc.php")


@pytest.fixture(scope="session", autouse=True)
def server_config(request, conf):
    replace_server_config(config['ftp']['host'], config['ftp']['username'], config['ftp']['password'])
    def fin():
        restore_server_config(config['ftp']['host'], config['ftp']['username'], config['ftp']['password'])
    request.addfinalizer(fin)


@pytest.fixture(scope="session")
def db(request, conf):
    db_config = config['db']
    dbfixture = DbFixture(host=db_config["host"], port=db_config["port"], database=db_config["database"], user=db_config["user"], password=db_config["password"])
    def fin():
        dbfixture.destroy()
    request.addfinalizer(fin)
    return dbfixture


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


def pytest_generate_tests(metafunc):
    for fixture in metafunc.fixturenames:
        if fixture.startswith("data_"):
            testdata = load_from_module(fixture[5:])
            metafunc.parametrize(fixture, testdata, ids=[str(x) for x in testdata])


def load_from_module(module):
    return importlib.import_module("data.%s" % module).testdata
