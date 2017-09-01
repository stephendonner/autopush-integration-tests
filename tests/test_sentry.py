import os
import time
import json

import pytest
import ipgetter
from raven import Client
from tests.client import request_rest
from tests.sentry import (
    issue_resolve_all,
    issue_id_latest,
    issue_items,
    remote_ip,
    string_clean,
    format_json
)


class TestSentry(object):

    @classmethod
    def setup_class(cls):
        print('\nSETUP: resolving any LogCheckErrors before testing\n')
        #issue_resolve_all(ISSUE_TITLE, SENTRY_TOKEN)

    @classmethod
    def teardown_class(cls):
        # this test relies on remote service (Sentry)
        # give ample time for issue to land before teardown
        print('\nTEARDOWN: resolving any LogCheckErrors...\n')
        #time.sleep(DELAY)
        #issue_resolve_all(ISSUE_TITLE, SENTRY_TOKEN)

    """

    def string_clean(self, s):
        s = str(s)
        return s.replace('"', '').replace("'", "")

    def remote_ip(self, obj_client_info):
        remote_ip = []
        for key, val in obj_client_info.iteritems():
            key_new = self.string_clean(key)
            val_new = self.string_clean(val)
            if key_new == 'remote_ip':
                ips = val_new.split(',')
                remote_ip = [ip for ip in ips if '172' not in ip]
        return remote_ip[0]


    def issue_items(self, variables):
        issue_id = issue_id_latest(ISSUE_TITLE, SENTRY_TOKEN)
        url = '{0}/api/0/issues/{1}/events/latest/'.format(HOST_SENTRY, issue_id)
        resp = request_rest(url, 'GET', SENTRY_TOKEN)
        params = []
        params.append(['release_project_name', resp['release']['projects'][0]['name']])
        params.append(['release_version', resp['release']['version']])
        params.append(['last_event', resp['release']['lastEvent']])
        params.append(['error_value', resp['metadata']['value']])
        params.append(['error_type', resp['metadata']['type']])

        r = resp['context']['client_info']
        #for key, val in r.iteritems():
        #    key_new = self.string_clean(key)
        #    val_new = self.string_clean(val)
        #    if key_new == 'remote_ip':
        #        ips = val_new.split(',')
        #        remote_ip = [x for x in ips if '172' not in x]
        #        params.append([key_new, remote_ip])
        remote_ip = self.remote_ip(r)
        params.append(['remote_ip', remote_ip])
        return params 
    """

        
    @pytest.mark.nondestructive
    def test_sentry_check(self, variables, request):

        # verify error on autopush side
        url_push_host_updates = variables['HOST_UPDATES']
        url_push_err = 'https://{0}/v1/err/crit'.format(url_push_host_updates)
        #assert resp['message'] == 'FAILURE:Success'
        #assert resp['error'] == 'Test Failure'
        
        # verify error Sentry side
        ext_ip = ipgetter.myip()
        print('EXT_IP: {0}'.format(ext_ip))

        #print('{0}'.format(json.dumps(resp,indent=4)))
        print('-------')
        resp = issue_items(variables)
        print(resp)

        # RELEASE VERSION
        # move this function to conftest
        # use github_release_tag in (test_url_checks)
        #release_version = resp['release']['version']
        
