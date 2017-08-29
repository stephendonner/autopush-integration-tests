import os
import time

import pytest
from raven import Client
from tests.client import request_rest
from tests.sentry import issue_resolve_all, format_json


DELAY = 10
SENTRY_TOKEN = os.environ['SENTRY_TOKEN']


class TestSentry(object):

    @classmethod
    def setup_class(cls):
        print('\nSETUP: resolving any LogCheckErrors before testing\n')
        issue_resolve_all('LogCheckError: LogCheck', SENTRY_TOKEN)

    @classmethod
    def teardown_class(cls):
        # this test relies on a remote service so we'll need to give
        # ample time for error to land in Sentry before teardown
        print('\nTEARDOWN: resolving any LogCheckErrors...\n')
        time.sleep(DELAY)
        issue_resolve_all('LogCheckError: LogCheck', SENTRY_TOKEN)

    @pytest.mark.nondestructive
    def test_sentry_check(self, variables, request):
        url_push_host_updates = variables['HOST_UPDATES']
        url_push_err = 'https://{0}/v1/err/crit'.format(url_push_host_updates)
        print(url_push_err)
        resp = request_rest(url_push_err, method='GET')
        resp = format_json(resp)
        print('{0}\n\n'.format(resp))

        resp = issue_resolve_all('LogCheckError: LogCheck', SENTRY_TOKEN)
        # assert something on this shit down here
        # we'll need to do a GET on the issue num created
        # then assert the IP
