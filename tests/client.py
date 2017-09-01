import sys
import json
import requests


def request_rest(url, method='GET', auth='', data=''):

    resp = ''
    headers = {'Content-Type': 'application/json'}

    if method == 'GET':
        resp = requests.get(url, auth=(auth, ''))
    elif method == 'DELETE':
        resp = requests.delete(url, auth=(auth, ''), headers=headers)
    elif method == 'PUT':
        resp = requests.put(
            url,
            auth=(auth, ''),
            data=json.dumps(data),
            headers=headers
        )
    else:
        sys.exit('ERROR! REST method: {0} - not supported. Aborting!', method)

    return resp.json()
