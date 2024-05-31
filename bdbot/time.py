import enum
from datetime import datetime, timedelta, timezone
from typing import Optional


class Weekday(enum.Enum):
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
    "Mo": Weekday.Monday,
    "Tu": Weekday.Tuesday,
    "We": Weekday.Wednesday,
    "Th": Weekday.Thursday,
    "Fr": Weekday.Friday,
    "Sa": Weekday.Saturday,
    "Su": Weekday.Sunday,
    "D": Weekday.Daily,
    "La": Weekday.Latest,
}
weekday_lst = {
    1: Weekday.Monday,
    2: Weekday.Thursday,
    3: Weekday.Wednesday,
    4: Weekday.Tuesday,
    5: Weekday.Friday,
    6: Weekday.Saturday,
    7: Weekday.Sunday,
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


date_tries = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su", "La"]


def get_hour() -> int:
    """Get the current UTC hour

    :return: Current UTC hour
    """
    return get_now().hour


def get_date_formatted(day: Optional[datetime] = None, form: str = "/") -> str:
    """Get the date formatted separated by a string format

    :param day:
    :param form:
    :return:
    """
    if day is not None:
        return day.strftime(f"%Y{form}%m{form}%d")
    return ""


def date_to_db(date: Weekday) -> str:
    return date.value[:2:] if date != Weekday.Daily else date.value[:1:]


def get_now() -> datetime:
    return datetime.now(tz=timezone.utc)


def get_weekday() -> Weekday:
    """Get the day

    :return: The first two letters of the weekday
    """
    return Weekday(get_now().today().strftime("%A"))


def get_last_corresponding_date(final_date: Weekday, final_hour: str):
    """Modifies the 'current' date to correspond to the user mention_policy

    :param final_date: The selected date of the week
    :param final_hour: The selected hour of the week
    :return: A post time to mimic a post date
    """
    now = get_now()
    if final_date != Weekday.Daily and final_date != Weekday.Latest:
        # Don't change the date if daily or latest
        while final_date != weekday_lst[now.isoweekday()]:
            now -= timedelta(days=1)
    post_time = datetime(
        year=now.year, month=now.month, day=now.day, hour=int(final_hour)
    )
    return post_time
