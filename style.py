import os

os.system("")  # switches on ANSI colors in older Windows consoles; harmless elsewhere

CODES = {
    "black": 30, "red": 31, "green": 32, "yellow": 33,
    "blue": 34, "magenta": 35, "cyan": 36, "white": 37, "gray": 90,
}
RESET = "\033[0m"


def color(name):
    """Return the escape code for a color name. Unknown names fall back to the default color."""
    return f"\033[{CODES.get(name, 39)}m"