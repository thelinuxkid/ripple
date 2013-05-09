import math

from dateutil import tz, parser
from datetime import datetime, timedelta

ripple_epoch = datetime(2000, 1, 1, tzinfo=tz.tzutc())

def drop(drops):
    """
    Converts a string to drops. A drop is the smallest unit in the Ripple
    currency (0.000001 XRP)
    """
    if not drops.isdigit():
        raise ValueError(
            'Value must be a positive integer: {drops}'.format(
                drops=drops,
            )
        )
    # Python will automatically cast to a long integer for any x such
    # that x < -sys.maxint-1 or x > sys.maxint
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

def utc_from_iso(dt_str, assume_local=False):
    """
    Convert an ISO-8601 formatted string to a datetime
    object. Timezone information must be present unless assume_local
    is True.
    """
    # dateutil.parser.parse returns today's date when fed the empty
    # string
    if dt_str == '':
        raise ValueError('Value cannot be empty string')
    dt = parser.parse(dt_str)
    if dt.tzinfo is None:
        if not assume_local:
            # We cannot convert to UTC without knowing a timezone A
            # lack of timezone implies local time.
            # http://en.wikipedia.org/wiki/ISO_8601#Time_zone_designators
            raise ValueError(
                'Value must contain timezone information: '
                '{dt}'.format(
                    dt=dt.isoformat(),
                )
            )
        dt = dt.replace(tzinfo=tz.tzlocal())

    if dt.tzinfo.utcoffset(dt) is not None:
        dt = dt.astimezone(tz.tzutc())
    return dt
