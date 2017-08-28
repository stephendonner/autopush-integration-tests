import os
import sys
import json
#from tests.request_helper import request
from request_helper import request


SENTRY_TOKEN = os.environ['SENTRY_TOKEN']
HOST_SENTRY = 'https://sentry.prod.mozaws.net'
ORGANIZATION= 'operations'
project_slug = 'Push/autopush-stage'
project_slug = 'autopush-stage'


def format_json(j):
    return json.dumps(j, indent=4)

def url_projects_list():
    return '{0}/api/0/projects/'.format(HOST_SENTRY)

def url_issues_list(project_slug):
    return '{0}/api/0/projects/{1}/{2}/issues/'.format(HOST_SENTRY, ORGANIZATION, project_slug )

def url_issue_update(num_issue):
    return '{0}/api/0/issues/{1}/'.format(HOST_SENTRY, num_issue)

def url_organizations():
    return '{0}/api/0/url_organizations/{1}/projects/'.format(HOST_SENTRY, ORGANIZATION) 

def issue_resolve_all(issue_title):
    url = url_issues_list(project_slug)
    issues = request(url, 'GET', SENTRY_TOKEN)

    for issue in issues:
        resp = format_json(issues)
        if issue['title'] == issue_title:
            if issue['status'] == 'unresolved':
                url = url_issue_update(issue['id'])
                resp = request(
                    url, 'PUT', SENTRY_TOKEN, {"status": "resolved"})
                resp = format_json(resp)
    return resp

def issues_list_all():
    url = url_issues_list(project_slug)
    resp = request(url, 'GET', SENTRY_TOKEN)
    #print(json.dumps(resp, indent=4))

print('--------------------')
print('BEFORE')
print('--------------------')

issues_list_all()

print('--------------------')

resp = issue_resolve_all('LogCheckError: LogCheck')
print(resp)
