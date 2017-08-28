import os
import sys
import json
import requests


SENTRY_TOKEN = os.environ['SENTRY_TOKEN']


def request(url, method='GET', auth='', data=''):
    headers = {'Content-Type': 'application/json'}
    if method == 'GET':
        return requests.get(url, auth=(auth, '')).json()
    elif method == 'DELETE':
        print('DELETE.....')
        return requests.delete(url, auth=(auth, ''), headers=headers).json()
    elif method == 'PUT':
        print('PUT.....')
        return requests.put(
            url,
            auth=(auth, ''),
            data=json.dumps(data),
            headers=headers
        ).json()
    else:
        print('ERROR! method: {0} - not supported. Aborting!', method)
        sys.exit()
