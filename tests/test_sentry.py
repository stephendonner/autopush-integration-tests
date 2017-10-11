import datetime
import ipgetter
import pytest

from tests.client import request_rest
from tests.sentry import (
    issue_resolve_all,
    issue_id_latest,
    issue_items,
    format_json
)
from tests.timeout import verify_timeout


ISSUE_TITLE = 'LogCheckError: LogCheck'


class TestSentry(object):

    @classmethod
    def setup_class(cls):
        print('\nSETUP: resolving any LogCheckErrors before testing\n')
        # issue_resolve_all(ISSUE_TITLE, SENTRY_TOKEN, PROJECT_SLUG)

    @classmethod
    def teardown_class(cls):
        # this test relies on remote service (Sentry)
        # give ample time for issue to land before teardown
        print('\nTEARDOWN: resolving any LogCheckErrors...\n')
        """
        time.sleep(DELAY)
        issue_resolve_all(ISSUE_TITLE, SENTRY_TOKEN, project_slug)
        """

    def assert_ok(self, msg='assert OK'):
        print(msg)
        return True

    @pytest.mark.nondestructive
    def test_sentry_check(self, variables, request, project_slug, release_version): # noqa

        # verify error on autopush side
        url_push_host_updates = variables['HOST_UPDATES']
        url = 'https://{0}/v1/err/crit'.format(url_push_host_updates)

        UTCNOW = datetime.datetime.utcnow()

        resp = request_rest(url, 'GET')
        assert resp['message'] == 'FAILURE:Success' and \
            self.assert_ok('FAILURE:Success'), \
            'Forced /err/crit unsuccessful!'
        assert resp['error'] == 'Test Failure' and \
            self.assert_ok('Test Failure - OK'), \
            'Unexpected error message!'

        # verify error Sentry side
        ip_ext = ipgetter.myip()
        issues = issue_items(variables, project_slug, ISSUE_TITLE)
        for item in issues:
            if item[0] == 'remote_ip':
                ip_remote = item[1]
                assert ip_ext == ip_remote and \
                    self.assert_ok('IP address match!'), \
                    'IP addresses don\'t match!'
            if item[0] == 'release_project_name':
                release_project_name = item[1]
                assert release_project_name == project_slug and \
                    self.assert_ok('Project slug matches!'), \
                    'Project slug doesn\'t match!'
            if item[0] == 'release_version':
                release_version_sentry = item[1]
                release_version_github = release_version
                assert release_version_sentry == release_version_github and \
                    self.assert_ok('Release version matches!'), \
                    'Release version doesn\'t match!'
            if item[0] == 'last_event':
                sentry_last_event = item[1]
                print('last_event: {0}'.format(sentry_last_event))
                time_verified = verify_timeout(UTCNOW, sentry_last_event)
                print('time_verified: {0}'.format(time_verified))
            """
                assert time_verified and \
                    self.assert_ok('Last event within time boundary!'), \
                    'Last event not within time boundary!'
            """
