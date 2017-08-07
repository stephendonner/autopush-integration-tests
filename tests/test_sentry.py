import os
import pytest
import globals as gbl
from raven import Client


@pytest.mark.nondestructive
def test_sentry_check():
    print(os.environ['URL_SENTRY'])
    assert(True)
