#   --------------------------------------------------------------------------------------------------------------------
#   ....................................................................................................................
#   Ⓒ by https://github.com/flashnuke Ⓒ................................................................................
#   --------------------------------------------------------------------------------------------------------------------
# todo names: pass-dict generator, dict-attack passgenerator, etc

import itertools
import argparse

from typing import List
from datetime import datetime
from utils import *


class Password:
    def __init__(self,
                 names_raw: List[str],
                 dates_raw: List[str],
                 number_raw: List[str],
                 locations_raw: List[str],
                 additional_raw: List[str]):
        # todo: impose pass limit, min and max... 8 and 32. dont truncate but just omit

        self._names_raw = names_raw
        self._dates_raw = dates_raw
        self._numbers_raw = number_raw
        self._locations_raw = locations_raw
        self._additional_raw = additional_raw

        combined = self._prepare_all_dicts()
        print_info("Initial words prepared before proceeding to the wordlist generation:")
        print_info(combined)

        # todo refactor all below to different method
        total = 0
        x = Password.power_set(combined)  # make a power set of all words
        total_set = set()
        for subset in x:
            a = '\t'.join(subset)
            aa = self.generate_variations(a)  # generate variations by using different separators
            total_set |= aa
            total += len(aa)

        print_info(total)
        with open("results.txt", "w") as output:
            output.write('\n'.join(sorted(total_set)))

    def _prepare_names(self):
        prepared = set()
        for name in self._names_raw:
            prepared.add(name.capitalize())
            prepared.add(self.decapitalize_str(name))
        return prepared

    def _prepare_dates(self): # todo accept list instead of using self.?
        # todo dates: if accepted input contains anything other than 0-9 and ., disregard it... also accept only
        # todo unknown year add: option to "d.m"
        #
        prepared = set()
        for date in self._dates_raw:
            if date:
                day, month, *args = date.split('.')
                if args:
                    year = args[0]
                    prepared.add(year)
                    prepared.add(year[2:])
                    prepared.add(year[:2])  # todo check if works

                for i in [day, month]:
                    if len(i) == 1:
                        prepared.add(f'0{day}')
                prepared.add(day)  # day
                prepared.add(month)

        return prepared

    def _prepare_numbers(self):
        # todo if contains anything other than numbers, disregard it...
        return set(self._numbers_raw)

    def _prepare_locations(self):
        prepared = set()
        for res in self._locations_raw:
            prepared.add(res.capitalize())
            prepared.add(self.decapitalize_str(res))
        return prepared

    def _prepare_additional(self):
        prepared = set()
        for word in self._additional_raw:
            prepared.add(word.capitalize())
            prepared.add(self.decapitalize_str(word))
        return prepared

    def _prepare_all_dicts(self):
        names = self._prepare_names()
        dates = self._prepare_dates()
        numbers = self._prepare_numbers()
        lcoations = self._prepare_locations()
        additional = self._prepare_additional()
        # todo above methods return the prepared rather than just prepare...
        return names | dates | numbers | lcoations | additional

    @staticmethod
    def decapitalize_str(word: str) -> str:
        return word[0].lower() + word[1:] if len(word) > 1 else word[0].lower()

    @staticmethod
    def power_set(val_set: set) -> list:
        """Generate powerset without empty set"""
        return [set(subset) for r in range(len(val_set) + 1)
                for subset in itertools.combinations(val_set, r)
                if len(subset) > 0]

    def generate_variations(self, inp: str) -> set:
        words = inp.split("\t") # todo \t define as macro somewhere
        separators = ['-', '.', '_']  # todo define separators as var
        # todo also in separator - add no separator

        sep_combinations = itertools.product(separators, repeat=len(words) - 1)
        variations = {''.join([word + sep for word, sep in zip(words, seps)] + [words[-1]])
                      for seps in sep_combinations}

        return {p_var for p_var in variations if self.is_pass_valid(p_var)}

    def is_pass_valid(self, password: str):
        return 8 <= len(password) <= 32

    @staticmethod
    def verify_dates_input(dates_lst: List[str]):
        for date in dates_lst:
            if date:
                if not Password.verify_date_format(date): # todo consider into InputValidator?
                    return False
        return True

    @staticmethod
    def verify_date_format(date_str):
        # todo verify while accepting input
        for pattern in ["%d.%m", "%d.%m.%Y"]:  # todo accepted patterns outside?
            try:
                datetime.strptime(date_str, pattern)
                return True
            except ValueError:
                continue
        return False

    @staticmethod
    def verify_numbers_input(numbers_str):
        for number in numbers_str:
            if number and not number.isdigit():  # todo consider into InputValidator?
                return False
        return True

    @staticmethod
    def separate_input(input_str: str) -> List[str]:
        return [i for i in input_str.split(" ") if i]  # filter out empty strings  # todo separator to var


if __name__ == "__main__":
    # x = Password("names_input", "dates_input", "numbers_input", "locations_input", "additional_input")

    printf(f"\n{BANNER}\n"
           f"Make sure of the following:\n"
           f"1. Disregard capital letters (at the beginning of words)\n" # todo at the vs in the
           f"2. Write two-letter words as two words (i.e \"new york\")\n"
           f"Written by {BOLD}@flashnuke{RESET}")
    printf(DELIM)
    # restore_print()

    parser = argparse.ArgumentParser(description='todo')  #
    # todo argparse = min pass and max pass
    pargs = parser.parse_args()

    # invalidate_print()  # after arg parsing
    print_info(f"{BOLD}When providing several words, separate them using a whitespace{RESET}")
    names_input = Password.separate_input(print_input("Enter meaningful names (i.e: First/Last names, nickname, pet name, etc):"))

    dates_input = Password.separate_input(print_input("Enter meaningful dates [DAY.MONTH.YEAR] (i.e: 24.02.2002, 31.03, etc):"))
    while not Password.verify_dates_input(dates_input):
        print_error("Invalid datetime format. Please use the following format: \"%d.%m\" or \"%d.%m.%Y\"")
        dates_input = Password.separate_input(print_input("Enter meaningful dates [DAY.MONTH.YEAR] (i.e: 24.02.2002, 31.03, etc):"))

    numbers_input = Password.separate_input(print_input("Enter meaningful numbers (from username, current year, etc):"))
    while not Password.verify_numbers_input(numbers_input):
        print_error("Invalid number format. Please enter digits only or nothing")
        numbers_input = Password.separate_input(print_input("Enter meaningful numbers (from username, current year, etc):"))

    locations_input = Password.separate_input(print_input("Enter meaningful locations (city of birth, residence, etc):"))
    additional_input = Password.separate_input(print_input("Enter misc words (any word you think might be of help and did not fit above):"))
    # todo handle extra whitespaces "word word   word word"
    printf(names_input)

    x = Password(names_input, dates_input, numbers_input, locations_input, additional_input)

    # todo info about computation time in readme
    # todo argparser no all lower or no all-upper

# Names:
#
#   First name
#   Last name
#   Nickname
#   Pet name
#
#   Any other names (middle names, nicknames)
#
#
# Numbers:
#
#   Day bday
#   Month bday
#   Year bday
#
#   Phone number
#
# Residence
#
#   Country
#   City
#
# Misc
#
#
# * current year down to birthday
# * Option to substitue for special chars
