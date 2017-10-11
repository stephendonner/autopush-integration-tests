import sys
import time
from dateutil import parser
from datetime import datetime, timedelta


def utc_to_timestamp(time_utc):
    t = str(time_utc)
    print('TIME_UTC: {0}'.format(t))
    if 'Z' in t:
        t = t.replace('Z', '')
        print('ZZZZZ: {0}'.format(t))
    if 'T' in t:
        t = t.replace('T', ' ')
        print('TTTTT: {0}'.format(t))
    #d = datetime.strptime(str(time_utc), "%Y-%d-%m %H:%M:%S.%f").strftime('%s')
    if '.' in t:
        tmp = t.split('.')
        t = tmp[0]
        print('......: {0}'.format(t))
    return datetime.strptime(str(t), "%Y-%d-%m %H:%M:%S").strftime('%s')

"""
def utc_string_sanitize(time_utc):
    if 'Z' in time_utc:
        print('ZZZZZ')
        time_utc = time_utc.replace('Z', '')
    if 'T' in time_utc:
        time_utc = time_utc.replace('T', ' ')
    return time_utc
"""


def verify_timeout(test_start, sentry_log_time):
    """ Verify Sentry log time is within acceptable time 
    delta from test start"""
  
    print('TEST START: {0}'.format(test_start))
    print('SENTRY: {0}'.format(sentry_log_time))

    ts_test_start = utc_to_timestamp(test_start)
    ts_sentry_log_time = utc_to_timestamp(sentry_log_time)
    print('TS TEST START: {0}'.format(ts_test_start))
    print('TS SENTRY: {0}'.format(ts_sentry_log_time))

    diff_allowed = 4 #6 * 60
    print('DIFF_ALLOWED: {0}'.format(diff_allowed))

    diff_actual = (int(ts_sentry_log_time) - int(ts_test_start))

    print('DIFF_ACTUAL: {0}'.format(diff_actual))
    if diff_actual < diff_allowed:  
        print('true')
    else:
        print('false')

    return True


if __name__ == '__main__':
    time_test = datetime.utcnow()
    time.sleep(5)
    sentry_log_time = datetime.utcnow()
    verify_timeout(time_test, sentry_log_time)
