#   --------------------------------------------------------------------------------------------------------------------
#   ....................................................................................................................
#   Ⓒ by https://github.com/flashnuke Ⓒ................................................................................
#   --------------------------------------------------------------------------------------------------------------------
# todo names: pass-dict generator, dict-attack passgenerator, etc

import itertools
import argparse

from utils import *


class Password:
    def __init__(self,
                 names_raw: List[str],
                 dates_raw: List[str],
                 number_raw: List[str],
                 locations_raw: List[str],
                 additional_raw: List[str],
                 pass_minlen: int,
                 pass_maxlen: int,
                 word_separators: str):
        self._names_raw = names_raw
        self._dates_raw = dates_raw
        self._numbers_raw = number_raw
        self._locations_raw = locations_raw
        self._additional_raw = additional_raw

        self._pass_minlen = pass_minlen
        self._pass_maxlen = pass_maxlen

        self._word_separators = [i for i in word_separators]
        self._word_separators.append('')
        print_info(f"separators chosed -> '{self._word_separators}'")

        combined = self._prepare_all_dicts()
        print_info("Initial words prepared before proceeding to the wordlist generation:")
        print_info(combined)

        # todo refactor all below to different method
        total = 0
        x = Password.power_set(combined)  # make a power set of all words
        total_set = set()
        for subset in x:
            total_len = 0
            for sss in subset:
                total_len += len(sss)
            if not self.is_pass_length_valid(total_len):
                print_info(subset)
                continue

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

    def _prepare_dates(self):
        # todo dates: if accepted input contains anything other than 0-9 and ., disregard it... also accept only
        # todo unknown year add: option to "d.m"
        #
        prepared = set()
        for date in self._dates_raw:
            print_info(self._dates_raw)
            if date:
                print_info(date)
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
        words = inp.split("\t")  # todo \t define as macro somewhere
        separators = ['', '-', '.', '_']  # todo define separators as var
        # todo also in separator - add no separator

        sep_combinations = itertools.product(separators, repeat=len(words) - 1)
        variations = {''.join([word + sep for word, sep in zip(words, seps)] + [words[-1]])
                      for seps in sep_combinations}

        return {p_var for p_var in variations if self.is_pass_length_valid(len(p_var))}

    def is_pass_length_valid(self, password_len: int):
        return self._pass_minlen <= password_len <= self._pass_maxlen


if __name__ == "__main__":
    # x = Password(separate_input("bayan bill"),
    #              separate_input("30.01.1980"),
    #              separate_input("12"),
    #              separate_input("georgia"),
    #              separate_input("narnia"),
    #              DEF_PASS_LEN_MIN,
                 # DEF_PASS_LEN_MAX)
    # exit(0)

    printf(f"\n{BANNER}\n"
           f"Make sure of the following:\n"
           f"1. Disregard capital letters (at the beginning of words)\n"  # todo at the vs in the
           f"2. Write two-letter words as two words (i.e \"new york\")\n"
           f"Written by {BOLD}@flashnuke{RESET}")
    printf(DELIM)
    # restore_print()

    parser = argparse.ArgumentParser(description='todo')  #
    parser.add_argument("-m", "--min-len", dest='pass_minlen', type=int, metavar=(""), default=DEF_PASS_LEN_MIN,
                        help=f"minimum pass length (default -> {DEF_PASS_LEN_MIN})",
                        required=False)
    parser.add_argument("-x", "--max-len", dest='pass_maxlen', type=int, metavar=(""), default=DEF_PASS_LEN_MAX,
                        help=f"maximum pass length (default -> {DEF_PASS_LEN_MAX})",
                        required=False)
    parser.add_argument("-s", "--seperators", dest='word_sep', type=str, metavar=(""), default=DEF_WORD_SEPARATORS,
                        help=f"word separators for password generation (default -> {DEF_WORD_SEPARATORS})",
                        required=False)
    # todo argparse = min pass and max pass
    pargs = parser.parse_args()

    # invalidate_print()  # after arg parsing
    print_info(f"{BOLD}When providing several words, separate them using a whitespace{RESET}")
    names_input = input_validator("Enter meaningful names (i.e: First/Last names, nickname, pet name, etc):")
    dates_input = input_validator("Enter meaningful dates [DAY.MONTH.YEAR] (i.e: 24.02.2002, 31.03, etc):",
                                  "Invalid datetime format. Please use the following format:"
                                  " \"%d.%m\" or \"%d.%m.%Y\"",
                                  verify_dates_input)
    numbers_input = input_validator("Enter meaningful numbers (from username, current year, etc):",
                                    "Invalid number format. Please enter digits only or nothing",
                                    verify_numbers_input)
    locations_input = input_validator("Enter meaningful locations (city of birth, residence, etc):")
    additional_input = input_validator("Enter misc words (any word you think might be of help and did not fit above):")
    # todo handle extra whitespaces "word word   word word"
    # todo print separators in init
    printf(names_input)
    printf(pargs.pass_maxlen)

    x = Password(names_input, dates_input, numbers_input, locations_input, additional_input, pargs.pass_minlen, pargs.pass_maxlen,
                 pargs.word_sep)

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
