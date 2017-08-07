import json
import requests

REQUEST_TIMEOUT = 3.0
LINE = '----------------------------'


def _header_label(test_name,  env=''):

    if env:
        env = '({0})'.format(env.upper())
    label = '{0} {1}'.format(test_name, env)
    return '{0}\n{1}\n{2}\n\n'.format(LINE, label, LINE)

def _http_request(url):
    # requests: r.status_code, r.headers, r.content

    out = ''

    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        response_time = requests.get(url).elapsed.total_seconds()
        if response.history:
            out += "Request was redirected!\n"
            for resp in response.history:
                print(resp.status_code, resp.url)
            out += 'status code: {0} --> destination: {1}\n'.format(
                response.status_code, response.url)
        else:
            try:
                j = json.loads(response.content)
                out += json.dumps(j, indent=4)
            except ValueError:
                out = response.content
        out += '\nResponse time: {0}\n'.format(response_time)
    except requests.exceptions.Timeout:
        out += ">>> ERROR! Request timed out! <<<\n"
    return out + '\n\n'
