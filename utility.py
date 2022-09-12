import datetime as dt


def is_after(from_datetime: dt.datetime, to_datetime: dt.datetime) -> bool:
    if from_datetime.year == to_datetime.year:
        if from_datetime.month == to_datetime.month:
            if from_datetime.day == to_datetime.day:
                if from_datetime.hour == to_datetime.hour:
                    if from_datetime.minute == to_datetime.minute or from_datetime.minute < to_datetime.minute:
                        return False
                elif from_datetime.hour < to_datetime.hour:
                    return False
            elif from_datetime.day < to_datetime.day:
                return False
        elif from_datetime.month < to_datetime.month:
            return False
    elif from_datetime.year < to_datetime.year:
        return False
    return True
