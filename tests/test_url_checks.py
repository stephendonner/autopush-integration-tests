import pytest
import requests
from tests.ticket import format_results
from tests.release_notes import ReleaseNotes
import globals as gbl


@pytest.fixture(scope="module", autouse=True)
def github_release_tag(request, variables):

    if not gbl.release_num:
        notes = ReleaseNotes(
            variables['REPO_OWNER'],
            variables['APPLICATION'],
            variables['ENVIRONMENT']
        )
        gbl.release_num = notes.last_tag
    return gbl.release_num


def api_response(variables, path):
    URL = 'https://{0}/{1}'.format(variables['HOST_UPDATES'], path)
    return requests.get(URL)


def ticket_update(name_test, status):
    print('UPDATING TICKET #{0}'.format(gbl.ticket_num))
    comments = format_results(name_test, status)
    print(comments)


@pytest.mark.nondestructive
def test_status_check(variables, request):
    name_test = request.node.name
    status = api_response(variables, 'status').json()

    release_num = github_release_tag(request, variables)
    assert('OK' == status['status'])
    assert(release_num == status['version'])
    if gbl.ticket_num:
        ticket_update(gbl.ticket_num, name_test, status)


@pytest.mark.nondestructive
def test_health_check(variables, request):
    name_test = request.node.name
    status = api_response(variables, 'health').json()
    ROUTER = variables['ROUTER']
    STORAGE = variables['STORAGE']
    release_num = github_release_tag(request, variables)

    assert(0 == status['clients'])
    assert('OK' == status[ROUTER]['status'])
    assert('OK' == status[STORAGE]['status'])
    assert('OK' == status['status'])
    assert(release_num == status['version'])
    if gbl.ticket_num:
        ticket_update(gbl.ticket_num, name_test, status)
