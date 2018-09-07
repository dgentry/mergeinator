#!/usr/bin/env python3


from .mergeinator import WHT, GRN, YEL, RED, BLD, BLDWHT, BLDRED, NORMAL, RESET, DIM
from .mergeinator import merge
from .mergeinator import _dmark

# Shut up pyflakes' F401 with explicit list of exported names
__all__ = {WHT, GRN, YEL, RED, BLD, BLDWHT, BLDRED, NORMAL, RESET, DIM,
           merge, _dmark}
