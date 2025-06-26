from .const import WEEKDAYS, WEEKDAYS_REVERSED, MONTHS, CURRENT_YEAR


def is_leap_year(year: int) -> bool:
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def int_to_weekday(n: int) -> str:
    """Convert a number (1-7) to a corresponding weekday (1=Monday ... 7=Sunday)"""
    return WEEKDAYS[n]


def weekday_to_int(name: str) -> int:
    """"Convert weekday's name (case-insensitive) to a corresponding number (Monday=1 ... Sunday=7)"""
    return WEEKDAYS_REVERSED[name.lower()]


def int_to_month(n: int) -> str:
    """Convert a number (1-12) to a corresponding month (1=January ... 12=December)"""
    return MONTHS[n]


def get_month_day_count(month_name: str, year: int = CURRENT_YEAR) -> int:
    months_day_count = {'january': 31,
                        'february': 29 if is_leap_year(year) else 28,
                        'march': 31,
                        'april': 30,
                        'may': 31,
                        'june': 30,
                        'july': 31,
                        'august': 31,
                        'september': 30,
                        'october': 31,
                        'november': 30,
                        'december': 31}

    return months_day_count[month_name.lower()]


def get_month_day_count_n(month_index: int, year: int = CURRENT_YEAR) -> int:
    months_day_count = {1: 31,
                        2: 29 if is_leap_year(year) else 28,
                        3: 31,
                        4: 30,
                        5: 31,
                        6: 30,
                        7: 31,
                        8: 31,
                        9: 30,
                        10: 31,
                        11: 30,
                        12: 31}

    return months_day_count[month_index]
