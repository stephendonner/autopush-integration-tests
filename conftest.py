import os
import pytest
import requests

import globals as gbl


GITHUB_ORG = 'mozilla-services'
GITHUB_REPO = 'autopush'


@pytest.fixture(scope='session')
def rel_num():
    gbl.release_num = ''


def pytest_addoption(parser):
    parser.addini('ticket_num', help='Ticket number')
    parser.addoption(
        '--ticket-num',
        metavar='ticket',
        default=os.getenv('TICKET_NUM', None),
        help='Ticket number the tests should use')


@pytest.fixture(scope='session')
def ticket_num():
    """Returns the ticket number"""
    # config = request.config
    # return config.getoption('ticket_num')
    gbl.ticket_num = '12345668'


def get_tags(url):
    """Get all tags as json from Github API."""

    req = requests.get(url)
    try:
	if 'Not Found' in req.text:
	    raise NotFoundError
    except NotFoundError:
	err_header = self.output.get_header('ERROR')
	err_msg = '{0}\nNothing found at: \n{1}\nABORTING!\n\n'.format(
	    err_header, url)
	sys.exit(err_msg)
    else:
	return req


@pytest.fixture(scope='session')
def project_slug():
    return 'autopush-stage' 


@pytest.fixture(scope='session')
def release_version():
    print('call github API')
    url = 'https://api.github.com/repos/{0}/{1}/releases/latest'.format(GITHUB_ORG, GITHUB_REPO)
    req = get_tags(url)
    return req.json()['tag_name']
