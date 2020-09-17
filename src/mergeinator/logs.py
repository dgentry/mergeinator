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
