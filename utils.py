import datetime
import time

def validate_date(date_text):
    try:
        datetime.date.fromisoformat(date_text)
        return True
    except ValueError:
        return False

def convert_commit_date(date):
    dt = time.gmtime(date)
    return str(dt.tm_year) + "-" + str(dt.tm_mon) + "-" + str(dt.tm_mday)