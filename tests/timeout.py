import sys
import time
from dateutil import parser
from datetime import datetime, timedelta


DIFF_ALLOWED = 3 * 60 # 3 minutes (in case of clock skew)


def utc_to_timestamp(time_utc):
    """ Normalize UTC string then convert to timestamp. """
    t = str(time_utc)
    if 'Z' in t:
        t = t.replace('Z', '')
    if 'T' in t:
        t = t.replace('T', ' ')
    if '.' in t:
        t = t.split('.')[0]
    return datetime.strptime(str(t), "%Y-%d-%m %H:%M:%S").strftime('%s')


def verify_timeout(test_start, sentry_log_time):
    """ Verify Sentry log time is within acceptable time 
    delta from test start"""
  
    ts_test_start = utc_to_timestamp(test_start)
    ts_sentry_log_time = utc_to_timestamp(sentry_log_time)
    print('TS TEST START: {0}'.format(ts_test_start))
    print('TS SENTRY: {0}'.format(ts_sentry_log_time))

    print('DIFF_ALLOWED: {0}'.format(DIFF_ALLOWED))

    # take abs value in case of clock skew
    diff_actual = abs((int(ts_test_start) - int(ts_sentry_log_time)))

    print('DIFF_ACTUAL: {0}'.format(diff_actual))
    if diff_actual < DIFF_ALLOWED:  
        # print('true')
        return True
    else:
        # print('false')
        return False


if __name__ == '__main__':
    time_test = datetime.utcnow()
    time.sleep(5)
    sentry_log_time = datetime.utcnow()
    verify_timeout(time_test, sentry_log_time)
