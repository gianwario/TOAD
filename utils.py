import datetime
import time


def validate_date(date_text):
    try:
        datetime.date.fromisoformat(date_text)
        return True
    except ValueError:
        return False


def convert_date(date):
    dt = time.gmtime(date)
    return str(dt.tm_year) + "-" + str(dt.tm_mon) + "-" + str(dt.tm_mday)


def check_date_within_timewindow(community, date):
    return (
        community.data.start_date
        <= datetime.datetime.strptime(convert_date(date), "%Y-%m-%d")
        <= community.data.end_date
    )


def check_githubdate_within_timewindow(community, date):
    return (
        community.data.start_date
        <= datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
        <= community.data.end_date
    )


def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3
