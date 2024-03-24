from typing import Callable, List, Union
from datetime import datetime

from .output_manager import *

AcceptedDateFormats = ["%d.%m", "%d.%m.%Y"]
InputWordSeparator = " "


def verify_date_format(date_str):
    for pattern in AcceptedDateFormats:
        try:
            datetime.strptime(date_str, pattern)
            return True
        except ValueError:
            continue
    return False


def verify_dates_input(dates_lst: List[str]):
    for date in dates_lst:
        if date:
            if not verify_date_format(date):
                return False
    return True


def verify_numbers_input(numbers_str):
    for number in numbers_str:
        if number and not number.isdigit():
            return False
    return True


def separate_input(input_str: str) -> List[str]:
    return [i for i in input_str.split(InputWordSeparator) if i]  # filter out empty strings


def input_validator(input_text: str,
                    error_text: str = "",
                    check_mtd: Union[None, Callable] = None) -> List[str]:
    user_input = separate_input(print_input(input_text))
    while check_mtd is not None and not check_mtd(user_input):
        print_error(error_text)
        user_input = separate_input(print_input(input_text))
    return user_input
