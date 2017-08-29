import json
import sys

from tests.client import request_rest


HOST_SENTRY = 'https://sentry.prod.mozaws.net'
ORGANIZATION = 'operations'
project_slug = 'Push/autopush-stage'
project_slug = 'autopush-stage'


def format_json(j):
    return json.dumps(j, indent=4)


def url_projects_list():
    return '{0}/api/0/projects/'.format(HOST_SENTRY)


def url_issues_list(project_slug):
    return '{0}/api/0/projects/{1}/{2}/issues/'.format(
        HOST_SENTRY, ORGANIZATION, project_slug)


def url_issue_update(num_issue):
    return '{0}/api/0/issues/{1}/'.format(HOST_SENTRY, num_issue)


def url_organizations():
    return '{0}/api/0/url_organizations/{1}/projects/'.format(
        HOST_SENTRY, ORGANIZATION)


def issue_resolve_all(issue_title, SENTRY_TOKEN):
    url = url_issues_list(project_slug)
    issues = request_rest(url, 'GET', SENTRY_TOKEN)
    resp = format_json(issues)

    for issue in issues:
        #print('{0} - {1} - {2}'.format(issue['title'], issue['id'], issue['status'])) # noqa
        if issue['title'] == issue_title:
            url = url_issue_update(issue['id'])
            resp = request_rest(
                url, 'PUT', SENTRY_TOKEN, {"status":"resolved"})
            resp = format_json(resp)
    return resp


def issues_list_all(SENTRY_TOKEN):
    url = url_issues_list(project_slug)
    resp = request_rest(url, 'GET', SENTRY_TOKEN)
    return json.dumps(resp, indent=4)
