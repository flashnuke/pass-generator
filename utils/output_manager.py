import os
import sys

_DEVNULL = open(os.devnull, "w")
_ORIG_STDOUT = sys.stdout
_CLEAR_LINE = "\x1b[1A\x1b[2K"
DELIM = 80 * "="

RESET = '\033[0m'
BOLD = '\033[1m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = "\033[1;33m"
BLUE = '\033[34m'


def invalidate_print():
    global _DEVNULL
    sys.stdout = _DEVNULL


def restore_print():
    global _ORIG_STDOUT
    sys.stdout = _ORIG_STDOUT


def printf(text, end="\n"):
    global _ORIG_STDOUT, _DEVNULL
    sys.stdout = _ORIG_STDOUT
    print(text, end=end)
    sys.stdout = _DEVNULL


def clear_line(lines=1):
    printf(lines * _CLEAR_LINE)


def print_error(text):
    printf(f"[{BOLD}{RED}!{RESET}] {text}")


def print_info(text, end="\n"):
    printf(f"[{BOLD}{BLUE}*{RESET}] {text}", end=end)


def print_input(text):
    return input(printf(f"[{BOLD}{GREEN}>{RESET}] {text} "))


def print_cmd(text):
    printf(f"[{BOLD}{GREEN}>{RESET}] {text}")


BANNER = f"""
asdasd"""