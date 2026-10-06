import math
SIG_FIGS = 4
def sf(x, n=SIG_FIGS):
    """Round x to n significant figures and return it as a string with
    thousands separators, e.g. sf(1852.5) -> '1,850', sf(0.30488) -> '0.305'."""
    if x == 0 or not math.isfinite(x):
        return str(x)
    digits = n - int(math.floor(math.log10(abs(x)))) - 1
    r = round(x, digits)
    return f"{r:,.{max(digits, 0)}f}"