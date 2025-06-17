def is_leap_year(year: int) -> bool:
    if year % 4 == 0:
        if year % 100 == 0:
            if year % 400 == 0:
                return True
    return False


def int_to_weekday(n: int) -> str:
    mapping = {1: 'Monday',
               2: 'Tuesday',
               3: 'Wednesday',
               4: 'Thursday',
               5: 'Friday',
               6: 'Saturday',
               7: 'Sunday',
               }

    return mapping[n]


def weekday_to_int(n: str) -> int:
    mapping = {'Monday': 1,
               'Tuesday': 2,
               'Wednesday': 3,
               'Thursday': 4,
               'Friday': 5,
               'Saturday': 6,
               'Sunday': 7,
               }

    return mapping[n]


def int_to_month(n: int) -> str:
    mapping = {1: 'January',
               2: 'February',
               3: 'March',
               4: 'April',
               5: 'May',
               6: 'June',
               7: 'July',
               8: 'August',
               9: 'September',
               10: 'October',
               11: 'November',
               12: 'December',
               }

    return mapping[n]
