
def nice_delta(delta_s):
    """Return an approximate nice looking time delta string from delta (in seconds).

    To be exact, we would need the two actual dates, rather than the number of seconds
    between them.
    """

    years = int(delta_s / SECONDS_IN_YEAR)
    remainder = delta_s - (years * SECONDS_IN_YEAR)

    months = int(remainder / SECONDS_IN_MONTH)
    remainder -= months * SECONDS_IN_MONTH

    weeks = int(remainder / SECONDS_IN_WEEK)
    remainder -= weeks * SECONDS_IN_WEEK

    days = int(remainder / SECONDS_IN_DAY)
    remainder -= days * SECONDS_IN_DAY

    hours = int(remainder / SECONDS_IN_HOUR)
    remainder -= hours * SECONDS_IN_HOUR

    minutes = int(remainder / SECONDS_IN_MINUTE)
    remainder -= minutes * SECONDS_IN_MINUTE

    # Round to tenths of a second
    seconds = int(remainder * 10) / 10
    remainder -= int(seconds)

    if delta_s < 0.1:
        milliseconds = int(remainder * 1000)
        remainder -= milliseconds * 1000
        # Round to tenths of a microsecond
        microseconds = int(remainder * 10e6 * 10) / 10

    if delta_s < 0.01:
        return "infinitesimal "

    str = ""
    if years > 0:
        str = f"{years}Y "
    if months > 0:
        str += f"{months}M "
    if weeks > 0:
        str += f"{weeks}W "
    if days > 0:
        str += f"{days}d "
    if hours > 0:
        str += f"{hours}h "
    if minutes > 0:
        str += f"{minutes}m "
    if seconds > 0:
        str += f"{seconds}s "
    if not len(str) > 0:
        if milliseconds > 0:
            str += f"{milliseconds}ms "
        if not len(str) > 0:
            str += f"{microseconds}usec "
    return str


KB = 1024
MB = 1024 * KB
GB = 1024 * MB
# TB = 1024 * GB
# PB = 1024 * TB
# EB = 1024 * PB


def nice_size(bytes):
    """Report bytes in appropriate units for size: T, G, M, K."""
    if bytes > GB:
        return f"{int(bytes*GB/10)/10} GB"
    if bytes > MB:
        return f"{int(bytes*MB/10)/10} MB"
    if bytes > KB:
        return f"{int(bytes*10/KB)/10} KB"
    return f"{bytes}B"

