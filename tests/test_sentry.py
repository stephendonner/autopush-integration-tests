import os
import pytest
from raven import Client
from tests.request_helper import request_rest
from tests.helper_sentry import issue_resolve_all, format_json

import globals as gbl


class TestSentry(object):


    def teardown_method(self, variables):
        print('TEARDOWN_METHOD!')
       
        SENTRY_TOKEN = os.environ['SENTRY_TOKEN']
        resp = issue_resolve_all('LogCheckError: LogCheck', SENTRY_TOKEN)

    @pytest.mark.nondestructive
    def test_sentry_check(self, variables, request):
        SENTRY_TOKEN = os.environ['SENTRY_TOKEN']
        url_push_host_updates = variables['HOST_UPDATES']
        url_push_err = 'https://{0}/v1/err/crit'.format(url_push_host_updates)
        resp = request_rest(url_push_err, method='GET')
        resp = format_json(resp) 
        print(resp)
        # assert something on this shit down here
        # we'll need to do a GET on the issue num created
        # then assert the IP
