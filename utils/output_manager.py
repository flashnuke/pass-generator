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
BRIGHT_BLUE = '\033[94m'


def print_error(text):
    print(f"[{BOLD}{RED}!{RESET}] {text}")


def print_info(text, end="\n"):
    print(f"[{BOLD}{YELLOW}*{RESET}] {text}", end=end)


def print_input(text):
    user_input = input(f"[{BOLD}{BLUE}>{RESET}] {text} {BRIGHT_BLUE}")
    sys.stdout.write(RESET)
    sys.stdout.flush()
    return user_input


def print_proc(text):
    print(f"[{BOLD}{GREEN}>{RESET}] {text}")


def print_empty(text):
    print(f"    {text}")


BANNER = f"""
{BOLD}{RED} _____{RESET}            {BOLD}{RED} _____{RESET}                           _             
{BOLD}{RED}| ___ \{RESET}           {BOLD}{RED}|  __ \{RESET}                         | |            
{BOLD}{RED}| |_/ /{RESET}_ _ ___ ___{BOLD}{RED}| |  \/{RESET} ___ _ __   ___ _ __ ____| |_ ___  ____ 
{BOLD}{RED}|  __/{RESET} _  / __/ __{BOLD}{RED}| | __ {RESET}/ _ \\ |_ \ / _ \\  __/ _  | __/ _ \|  __|
{BOLD}{RED}| |{RESET} | (_| \__ \__ {BOLD}{RED}\\ |_\\ \{RESET}  __/ | | |  __/ | | (_| | || (_) | |   
{BOLD}{RED}\_|{RESET}  \____|___/___/{BOLD}{RED}\____/{RESET}\___|_| |_|\___|_|  \__,_|\__\___/|_|   
"""
