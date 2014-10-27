from re import compile as re


NUMBER_RE = re('(\d*\.?\d*)')
CONVERT = {
    "bytes": (
        ("GB", 1000000000.0),
        ("MB", 1000000.0),
        ("KB", 1000.0),
    ),
    "short": (
        ("Tri", 1000000000000.0),
        ("Bil", 1000000000.0),
        ("Mil", 1000000.0),
        ("K",   1000.0),
    ),
    "s": (
        ("y", 31536000.0),
        ("M", 2592000.0),
        ("w", 604800.0),
        ("d", 86400.0),
        ("h", 3600.0),
        ("m", 60.0),
        ("s", 1.0),
        ("ms", 0.001),
    ),
    "percent": (
        ("%", 1),
        ("%", .01),
    )
}
CONVERT['ms'] = list((n, v * 1000) for n, v in CONVERT['s'])
CONVERT_HASH = {name: value for _types in CONVERT.values() for (name, value) in _types}
CONVERT_HASH['%'] = 1
TIME_UNIT_SIZE = dict(CONVERT['ms'])
TIME_UNIT_SYN = {"microsecond": "ms", "second": "s", "minute": "m", "hour": "h", "day": "d",
                 "week": "w", "month": "M", "year": "y"}
TIME_UNIT_SYN2 = dict([(v, n) for (n, v) in TIME_UNIT_SYN.items()])


def convert_to_format(value, frmt=None):
    units = CONVERT.get(frmt, [])
    for name, size in units:
        if size < value:
            break
    else:
        return value

    if size != 1:
        value /= size
        value = ("%.1f" % value).rstrip('0').rstrip('.')
    return "%s%s" % (value, name)


def convert_from_format(value):
    _, num, unit = NUMBER_RE.split(str(value))
    if not unit:
        return value
    return float(num) * CONVERT_HASH.get(unit, 1)


def parse_interval(interval):
    _, num, unit = NUMBER_RE.split(interval)
    num = float(num)
    return num * TIME_UNIT_SIZE.get(unit, TIME_UNIT_SIZE[TIME_UNIT_SYN.get(unit, 's')])


def interval_to_graphite(interval):
    _, num, unit = NUMBER_RE.split(interval)
    unit = TIME_UNIT_SYN2.get(unit, unit) or 'second'
    return num + unit