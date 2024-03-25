#   --------------------------------------------------------------------------------------------------------------------
#   ....................................................................................................................
#   Ⓒ by https://github.com/flashnuke Ⓒ................................................................................
#   --------------------------------------------------------------------------------------------------------------------
# todo names: pass-dict generator, dict-attack passgenerator, etc
import itertools
import time

from typing import Set, Tuple
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
                 word_separators: str,
                 output_filepath: str,
                 min_digits: int,  # todo document minimums... and state default
                 min_uppers: int,
                 min_lowers: int,
                 min_specials: int):
        self._names_raw = names_raw
        self._dates_raw = dates_raw
        self._numbers_raw = number_raw
        self._locations_raw = locations_raw
        self._additional_raw = additional_raw

        self._pass_minlen = pass_minlen
        self._pass_maxlen = pass_maxlen

        self._word_separators = [i for i in word_separators]
        self._word_separators.append('')

        self._output_filepath = output_filepath
        if os.path.exists(self._output_filepath):
            print(f"The path '{self._output_filepath}' exists.")
        else:
            print(f"The path '{self._output_filepath}' does not exist.")

        self._min_digits = min_digits
        self._min_uppers = min_uppers
        self._min_lowers = min_lowers
        self._min_specials = min_specials

    def generate_wordlist(self):
        start_t_sec = int(time.time())
        combined = self._prepare_all_dicts()
        print_info("Initial words prepared before proceeding to the wordlist generation:")
        print_info(combined)
        print_info(f"separators chosen -> {self._word_separators}")

        powerset_combined = Password.power_set(combined)  # make a power set of all words
        total_set = set()
        for subset in powerset_combined:
            total_subset_len = 0
            for word in subset:
                total_subset_len += len(word)
            if total_subset_len > self._pass_maxlen:
                continue
            aa = self._generate_variations(list(subset))  # generate variations by using different separators
            total_set |= aa

        finish_t_sec = int(time.time())
        print_info(f"finished after {finish_t_sec - start_t_sec}[sec]")
        self._save_results(total_set)

    def _save_results(self, total_set):
        print_info(f"saving {len(total_set)} words to {self._output_filepath}...")
        output = '\n'.join(sorted(total_set))
        try:
            self._write_to_file(self._output_filepath, output)
        except Exception as exc:
            print_error(f"exception occurred while writing results -> {exc}")
            if self._output_filepath != DEF_OUTPUT_FILEPATH:
                print_info(f"attempting to write to default output filepath instead -> {DEF_OUTPUT_FILEPATH}")
                try:
                    self._write_to_file(DEF_OUTPUT_FILEPATH, output)
                except Exception as exc:
                    print_error(f"unable to save output")

    @staticmethod
    def _write_to_file(filepath: str, output):
        with open(filepath, "w") as f:
            f.write(output)

    def _prepare_names(self) -> Set[str]:
        prepared = set()
        for name in self._names_raw:
            prepared.add(name.capitalize())
            prepared.add(self.decapitalize_str(name))
        return prepared

    def _prepare_dates(self) -> Set[str]:
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
                    prepared.add(year[:2])

                for i in [day, month]:
                    if len(i) == 1:
                        prepared.add(f'0{day}')
                prepared.add(day)  # day
                prepared.add(month)

        return prepared

    def _prepare_numbers(self) -> Set[str]:
        return set(self._numbers_raw)

    def _prepare_locations(self) -> Set[str]:
        prepared = set()
        for res in self._locations_raw:
            prepared.add(res.capitalize())
            prepared.add(self.decapitalize_str(res))
        return prepared

    def _prepare_additional(self) -> Set[str]:
        prepared = set()
        for word in self._additional_raw:
            prepared.add(word.capitalize())
            prepared.add(self.decapitalize_str(word))
        return prepared

    def _prepare_all_dicts(self) -> Set:
        names = self._prepare_names()
        dates = self._prepare_dates()
        numbers = self._prepare_numbers()
        lcoations = self._prepare_locations()
        additional = self._prepare_additional()

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

    def _generate_variations(self, words: List[str]) -> Set[str]:
        sep_combinations = itertools.product(self._word_separators, repeat=len(words) - 1)
        variations = {''.join([word + sep for word, sep in zip(words, seps)] + [words[-1]])
                      for seps in sep_combinations}
        return {p_var for p_var in variations if self._is_pass_valid(p_var)}

    def _is_pass_valid(self, password: str) -> bool:
        """
            performs the following checks on the password:
                * accepted length
                * minimum digits
                * minimum upper case letters
                * minimum lower case letters
                * minimum special characters
        """
        return self._pass_minlen <= len(password) <= self._pass_maxlen \
            and (sum(c.isdigit() for c in password) >= self._min_digits if self._min_digits > 0 else True) \
            and (sum(c.isupper() for c in password) >= self._min_uppers if self._min_uppers > 0 else True) \
            and (sum(c.islower() for c in password) >= self._min_lowers if self._min_lowers > 0 else True) \
            and (sum(not c.isalnum() for c in password) >= self._min_specials if self._min_specials > 0 else True)


if __name__ == "__main__":
    x = Password(separate_input("bayan bill"),
                 separate_input("30.01.1980"),
                 separate_input("12"),
                 separate_input("georgia"),
                 separate_input("narnia"),
                 DEF_PASS_LEN_MIN,
                 DEF_PASS_LEN_MAX,
                 "-.",
                 DEF_OUTPUT_FILEPATH,
                 DEF_MIN_DIGITS,
                 DEF_MIN_UPPERS,
                 DEF_MIN_LOWERS,
                 DEF_MIN_SPECIALS)
    x.generate_wordlist()
    exit(0)

    printf(f"\n{BANNER}\n"
           f"Make sure of the following:\n"
           f"1. Disregard capital letters (at the beginning of words)\n"  # todo at the vs in the
           f"2. Write two-letter words as two words (i.e \"new york\")\n"
           f"Written by {BOLD}@flashnuke{RESET}")
    printf(DELIM)
    # restore_print() # todo is this even needed?

    pargs = define_args()

    # invalidate_print()  # after arg parsing # todo is this even needed?
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
    printf(names_input)
    printf(pargs.pass_maxlen)

    x = Password(names_input, dates_input, numbers_input, locations_input, additional_input, pargs.pass_minlen,
                 pargs.pass_maxlen,
                 pargs.word_sep, pargs.output_path, pargs.min_digits, pargs.min_uppwers, pargs.min_lowers,
                 pargs.min_specials)
    x.generate_wordlist()

    # todo info about computation time in readme
    # todo argparser no all lower or no all-upper
    # todo min lower/upper param

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
