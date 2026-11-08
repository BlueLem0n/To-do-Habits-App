from datetime import datetime

DATE_FORMAT = "%d.%m.%Y %H:%M"


def format_datetime(dt: datetime | None) -> str | None:
    if dt is None:
        return None
    return dt.strftime(DATE_FORMAT)