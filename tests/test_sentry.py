import os
import pytest
import globals as gbl
from raven import Client


@pytest.mark.nondestructive
def test_sentry_check():
    print(os.environ['URL_SENTRY'])
    url_sentry = os.environ['URL_SENTRY']
    client = Client(url_sentry)
    try:
        1/0
    except ZeroDivisionError:
        client.captureException()
    assert(True)
