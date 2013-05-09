import math

from dateutil import tz
from datetime import datetime, timedelta

ripple_epoch = datetime(2000, 1, 1, tzinfo=tz.tzutc())

def drop(drops):
    """
    Converts a string to drops. A drop the smallest unit in the Ripple
    currency (0.000001 XRP)
    """
    if not drops.isdigit():
        raise ValueError(
            'Value must be a positive integer: {drops}'.format(
                drops=drops,
            )
        )
    # Python will automatically cast to long integer for any value not
    # in -sys.maxint - 1 <= x <= sys.maxint
    drops = int(drops)
    return drops

def totime(dt):
    """
    Converts a datetime object to the number of seconds since
    the Ripple epoch. The Ripple epoch is 946684800 seconds after the
    Unix epoch or 2000-01-01T00:00:00+00:00
    """
    if dt.tzinfo is None:
        # We cannot convert to UTC without knowing a timezone
        # A lack of timezone implies local time.
        # http://en.wikipedia.org/wiki/ISO_8601#Time_zone_designators
        raise ValueError(
            'Value must contain timezone information: '
            '{dt}'.format(
                dt=dt.isoformat(),
            )
        )
    if dt < ripple_epoch:
        raise ValueError(
            'Value cannot be earlier than {epoch}: {dt}'.format(
                epoch=ripple_epoch.isoformat(),
                dt=dt.isoformat(),
            )
        )
    dt = dt - ripple_epoch
    dt = dt.total_seconds()
    dt = math.ceil(dt)
    return long(dt)

def fromtime(seconds):
    """
    Converts the number of seconds since the Ripple epoch to a
    datetime object. The Ripple epoch is 946684800 seconds after the
    Unix epoch or 2000-01-01T00:00:00+00:00
    """
    dt = ripple_epoch + timedelta(seconds=seconds)
    return dt
