import configparser
import os
import pytest
import ssl
import globals as gbl


# Hack because of how SSL certificates are verified by default in Python
if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context


@pytest.fixture(scope='session')
def rel_num():
    gbl.release_num = ''


@pytest.fixture(scope='session')
def ticket_num():
    """Returns the ticket number"""
    # config = request.config
    # return config.getoption('ticket_num')
    gbl.ticket_num = '12345668'


def pytest_addoption(parser):
    parser.addini('ticket_num', help='Ticket number')
    parser.addoption(
        '--ticket-num',
        metavar='ticket',
        default=os.getenv('TICKET_NUM', None),
        help='Ticket number the tests should use')
    parser.addoption(
        "--env",
        dest="env",
        default="stage",
        help="Environment tests are running in: dev | stage | prod"
    )
    parser.addoption(
        "--api-version",
        dest="apiversion",
        default="0.0.0",
        help="Version of the autopush service API we are testing against"
    )


@pytest.fixture()
def env(request):
    return request.config.getoption("--env")


@pytest.fixture()
def apiversion(request):
    return request.config.getoption("--api-version")


@pytest.fixture()
def conf():
    config = configparser.ConfigParser()
    config.read('manifest.ini')
    return config
