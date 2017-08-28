import os

import pytest
from raven import Client
import requests

import globals as gbl


@pytest.mark.nondestructive
#def test_sentry_check():
def test_sentry_check(variables):
    #print(os.environ['HOST_UPDATES'])
    #url_push_host_updates = os.environ['HOST_UPDATES']
    print(variables['HOST_UPDATES'])
    url_push_host_updates = variables['HOST_UPDATES']
    url_push_err = 'https://{0}/v1/err/crit'.format(url_push_host_updates)
    #client = Client(url_push_err)

    try:
        1/0
    except ZeroDivisionError:
        client.captureException()
    assert(True)
