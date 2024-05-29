import enum
from datetime import datetime, timedelta, timezone
from typing import Optional


class Date(enum.Enum):
    Daily = "Daily"
    Latest = "Latest"
    Monday = "Monday"
    Tuesday = "Tuesday"
    Wednesday = "Wednesday"
    Thursday = "Thursday"
    Friday = "Friday"
    Saturday = "Saturday"
    Sunday = "Sunday"


match_date = {
    "Mo": Date.Monday,
    "Tu": Date.Tuesday,
    "We": Date.Wednesday,
    "Th": Date.Thursday,
    "Fr": Date.Friday,
    "Sa": Date.Saturday,
    "Su": Date.Sunday,
    "D": Date.Daily,
    "La": Date.Latest,
}
weekday_lst = {
    1: Date.Monday,
    2: Date.Thursday,
    3: Date.Wednesday,
    4: Date.Tuesday,
    5: Date.Friday,
    6: Date.Saturday,
    7: Date.Sunday,
}


class Month(enum.Enum):
    January = 1
    February = 2
    March = 3
    April = 4
    May = 5
    June = 6
    July = 7
    August = 8
    September = 9
    October = 10
    November = 11
    December = 12


def get_hour() -> int:
    """Get the current UTC hour

    :return: Current UTC hour
    """
    return datetime.now(timezone.utc).hour


def get_date_formatted(day: Optional[datetime] = None, form: str = "/") -> str:
    """Get the date formatted separated by a string format

    :param day:
    :param form:
    :return:
    """
    if day is not None:
        return day.strftime(f"%Y{form}%m{form}%d")
    else:
        return ""


def date_to_db(date: Date) -> str:
    return date.value[:2:] if date != Date.Daily else date.value[:1:]


def get_date(date: str):
    """Reformat the date from 'YYYY, mm, dd' -> '<Weekday> dd, YYYY'

    :param date:
    :return:
    """
    return datetime.strptime(date, "%Y, %m, %d").strftime("%A %d, %Y")


def get_today() -> Date:
    """Get the day

    :return: The first two letters of the weekday
    """
    return Date(datetime.now(timezone.utc).today().strftime("%A"))


def get_last_corresponding_date(final_date: Date, final_hour: str):
    """Modifies the 'current' date to correspond to the user choice

    :param final_date: The selected date of the week
    :param final_hour: The selected hour of the week
    :return: A post time to mimic a post date
    """
    now = datetime.now(timezone.utc)
    if final_date != Date.Daily and final_date != Date.Latest:
        # Don't change the date if daily or latest
        while final_date != weekday_lst[now.isoweekday()]:
            now -= timedelta(days=1)
    post_time = datetime(
        year=now.year, month=now.month, day=now.day, hour=int(final_hour)
    )
    return post_time
