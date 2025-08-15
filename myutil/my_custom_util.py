# Keep it simple for Dataproc Workshop example. However, the module can be of any complexity.

from datetime import datetime
from dateutil.relativedelta import relativedelta


# This function simply returns the number of years between the input_date and current date.
def myutil_calc_tenure(input_date):
    now = datetime.now()    
    diff = relativedelta(now, input_date)
    return diff.years


# This function returns a category description of a given tenure value in years
def myutil_tenure_category(years):
    if years <= 5:
        retval = "Short"
    elif years <= 15:
        retval = "Average"
    else:
        retval = "Long"
    
    return retval
