import dateutil.parser
import datetime
import sys


TIMEOUT_MINS = 5
UTCNOW = datetime.datetime.utcnow()

def is_timeout_exceeded(test_start_time):

    # BOGUS values for testing
    dt_stamp_sentry = UTCNOW +datetime.timedelta(minutes = 10)
    dt_stamp_test_start = test_start_time 

    # time measured on Sentry
    # ['contexts']['dateCreated']

    dt_timeout_period = dt_stamp_test_start + datetime.timedelta(minutes = TIMEOUT_MINS)

    print('start: ', test_start_time)
    print('timeout: ', dt_timeout_period)
    print('-----')
    print('sentry: ', dt_stamp_sentry)
    if dt_stamp_sentry < dt_timeout_period:
        return False 
    else:
        return True 


test_start_time = datetime.datetime.utcnow()
resp = is_timeout_exceeded(test_start_time)
print(resp)
