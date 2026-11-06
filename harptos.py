# List of the 12 months in the Calendar of Harptos in DnD
MONTHS = [
    "Hammer", "Alturiak", "Ches", "Tarsakh", "Mirtul", "Kythorn",
    "Flamerule", "Eleasis", "Eleint", "Marpenoth", "Uktar", "Nightal",
]

YEARS = range(1490, 1501)      # 1490 to 1500; change here when the campaign moves on

def is_valid(year, month, day):
    return year in YEARS and 1 <= month <= 12 and 1 <= day <= 30


def format_date(year, month, day):
    """Turn numbers into text like '12 Kythorn, 1492 DR'."""
    if year is None or month is None or day is None:
        return "no date"          # for payouts saved before this feature
    return f"{day} {MONTHS[month - 1]}, {year} DR"