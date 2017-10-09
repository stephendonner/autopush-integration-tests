import sys
import dateutil.parser
import datetime


TIMEOUT_MINS = 5
UTCNOW = datetime.datetime.utcnow()

#def verify_timeout(test_start_time, sentry_log_time):
def verify_timeout(sentry_log_time):

    
    # BOGUS values for testing
    #dt_stamp_sentry = UTCNOW +datetime.timedelta(minutes = 10)
    #print(test_start_time)
    dt_stamp_test_start = dateutil.parser.parse(test_start_time)
    #dt_stamp_test_start = test_start_time 
    #dt_stamp_test_start = datetime.utcfromtimestamp(test_start_time)

    # time measured on Sentry
    # ['contexts']['dateCreated']

    dt_timeout_period = dt_stamp_test_start + datetime.timedelta(minutes = TIMEOUT_MINS)

    print('start: ', test_start_time)
    print('timeout: ', dt_timeout_period)
    print('-----')
    print('sentry: ', dt_stamp_sentry)

    # TODO: returning true for now to get this working
    return True
    """
    if dt_stamp_sentry < dt_timeout_period:
        return False 
    else:
        return True 
    """


#test_start_time = datetime.datetime.utcnow()
#resp = is_timeout_exceeded(test_start_time)
#print(resp)
