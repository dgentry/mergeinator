from colored import fg, style
from os import environ, path
from sys import stdout
from datetime import datetime as dt

# Let's use ANSI escape sequence colors if we're on a tty
if stdout.isatty() or ('TERM' in environ and 'color' in environ['TERM']):
    WHT = fg('white')
    GRN = fg('green')
    YEL = fg('yellow')
    RED = fg('red')
    BLD = style(name="BOLD")
    NORMAL = style(name="RESET")
    RESET = "\x1b[39m"
    DIM = style(name="DIM")
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


def log(*args, **kwargs):
    mode = "w+"
    if path.isfile("merge.log"):
        mode = "a"
    with open("merge.log", mode) as global_log:
        print(dt.now().isoformat(), *args, file=global_log, **kwargs)


def ui(*args, **kwargs):
    print(*args, **kwargs)
    log(*args, **kwargs)
