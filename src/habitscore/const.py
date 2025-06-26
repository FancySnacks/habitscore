import pathlib
import datetime

SRC_PATH = pathlib.Path(__file__).resolve().parent
PROJECT_ROOT = SRC_PATH.parent.parent
PRESET_SAVE_PATH = PROJECT_ROOT / "data" / "presets"


# ===== Date & Time ===== #

NOW = datetime.datetime.now()
CURRENT_YEAR: int = NOW.year


WEEKDAYS = {
    1: 'monday', 2: 'tuesday', 3: 'wednesday',
    4: 'thursday', 5: 'friday', 6: 'saturday', 7: 'sunday'
}

WEEKDAYS_REVERSED: dict[str: int] = {v: k for k, v in WEEKDAYS.items()}

MONTHS = {
    1: 'january', 2: 'february', 3: 'march', 4: 'april',
    5: 'may', 6: 'june', 7: 'july', 8: 'august',
    9: 'september', 10: 'october', 11: 'november', 12: 'december'
}

MONTHS_REVERSED: dict[str: int] = {v: k for k, v in MONTHS.items()}
