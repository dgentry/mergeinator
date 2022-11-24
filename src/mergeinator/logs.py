from colored import fg, style
from os import environ
from sys import stdout

# Let's use ANSI escape sequence colors if we're on a tty
if stdout.isatty() or ('TERM' in environ and 'color' in environ['TERM']):
    WHT = fg('white')
    GRN = fg('green')
    YEL = fg('yellow')
    RED = fg('red')
    BLD = style.BOLD
    NORMAL = style.RESET
    RESET = "\x1b[39m"
    DIM = style.DIM
# But don't pollute a logfile with escape sequences
else:
    WHT = ''
    GRN = ''
    YEL = ''
    RED = ''
    BLD = ''
    NORMAL = ''
    RESET = ''
    DIM = ''
BLDWHT = BLD + WHT
BLDRED = BLD + RED


SECONDS_IN_MINUTE = 60
SECONDS_IN_HOUR = 60 * SECONDS_IN_MINUTE
SECONDS_IN_DAY = 24 * SECONDS_IN_HOUR
SECONDS_IN_WEEK = 7 * SECONDS_IN_DAY
# These are approximate:
SECONDS_IN_MONTH = 30 * SECONDS_IN_DAY
SECONDS_IN_YEAR = 365 * SECONDS_IN_DAY



def log(*args, **kwargs):
    mode = "w+"
    if os.path.isfile("merge.log"):
        mode = "a"
    with open("merge.log", mode) as global_log:
        print(dt.isoformat(dt.now()), *args, file=global_log, **kwargs)


def ui(*args, **kwargs):
    print(*args, **kwargs)
    log(*args, **kwargs)

