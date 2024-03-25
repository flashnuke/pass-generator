#!/usr/bin/env python3

import time
import itertools
import traceback

from utils import *
from typing import Set


#   --------------------------------------------------------------------------------------------------------------------
#   ..........................._____............._____..........................._......................................
#   ..........................| ___ \...........|  __ \.........................| |.....................................
#   ..........................| |_/ /_ _ ___ ___| |  \/ ___ _ __   ___ _ __ ____| |_ ___  ____..........................
#   ..........................|  __/ _  / __/ __| | __ / _ \ |_ \ / _ \  __/ _  | __/ _ \|  __|.........................
#   ..........................| | | (_| \__ \__ \ |_\ \  __/ | | |  __/ | | (_| | || (_) | |............................
#   ..........................\_|  \____|___/___/\____/\___|_| |_|\___|_|  \__,_|\__\___/|_|............................
#   ....................................................................................................................
#   Ⓒ by https://github.com/flashnuke Ⓒ................................................................................
#   --------------------------------------------------------------------------------------------------------------------


class PassGenerator:
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
                 min_specials: int,
                 dont_capitalize: bool):
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

        self._min_digits = min_digits
        self._min_uppers = min_uppers
        self._min_lowers = min_lowers
        self._min_specials = min_specials

        self._dont_capitalize = dont_capitalize

        self._print_settings()

    def _print_settings(self):
        print(DELIM)
        print_info(f"Password properties")
        print_empty(f"{self._pass_minlen} <= length <= {self._pass_maxlen}")
        print_empty(f"amount of digits >= {self._min_digits}")
        print_empty(f"amount of uppercase characters >= {self._min_uppers}")
        print_empty(f"amount of lowercase characters >= {self._min_lowers}")
        print_empty(f"amount of special characters >= {self._min_specials}")
        print_empty(f"add capitalized/un-capitalized versions of words -> {not self._dont_capitalize}")
        print(DELIM)

    def generate_wordlist(self):
        start_t_sec = int(time.time())
        combined = self._prepare_all_dicts()
        print_info(f"Words chosen -> {BOLD}{combined}{RESET}")
        print_info(f"Separators chosen -> {BOLD}{self._word_separators}{RESET}")
        print_proc(f"Creating subsets from words...")
        powerset_combined = PassGenerator.power_set(combined)  # make a power set of all words
        filtered_powerset_combined = self._filter_by_size(powerset_combined)  # no computations on irrelevant passwords
        print_proc(f"Starting to generate passwords from {BOLD}{len(filtered_powerset_combined)}{RESET} subsets")

        total_set = set()

        finished_ctr = 0
        last_reported_pct = 0
        total_passwords_generated = 0
        len_total_filtered_sets = sum(len(s) for s in filtered_powerset_combined)
        for subset in filtered_powerset_combined:
            finished_ctr += len(subset)
            variations = self._generate_variations(list(subset))  # generate variations by using different separators
            total_set |= variations
            total_passwords_generated += len(variations)

            finished_pct = int((finished_ctr / len_total_filtered_sets) * 100)
            if finished_pct % 10 == 0 and last_reported_pct != finished_pct:
                last_reported_pct = finished_pct
                print_proc(f"Status: generating [{finished_pct}% | {int(time.time()) - start_t_sec} sec], passwords generated so far: {BOLD}{total_passwords_generated}{RESET}")

        finish_t_sec = int(time.time())
        print_info(f"Status: finished after {BOLD}{finish_t_sec - start_t_sec}{RESET}[sec]")
        self._save_results(total_set)

    def _filter_by_size(self, power_set: List[Set[str]]) -> List[Set[str]]:
        filtered: List[Set[str]] = list()
        for subset in power_set:
            total_subset_len = 0
            for word in subset:
                total_subset_len += len(word)
            if total_subset_len <= self._pass_maxlen:
                filtered.append(subset)
        return filtered

    def _save_results(self, total_set):
        print(DELIM)
        print_proc(f"Saving {BOLD}{len(total_set)}{RESET} words to {BOLD}{os.path.abspath(self._output_filepath)}{RESET}")
        output = '\n'.join(sorted(total_set))
        try:
            self._write_to_file(self._output_filepath, output)
        except Exception as exc:
            print_error(f"Exception occurred while writing results -> {exc}")
            if self._output_filepath != DEF_OUTPUT_FILEPATH:
                print_info(f"Attempting to write to default output filepath instead -> {os.path.abspath(DEF_OUTPUT_FILEPATH)}")
                try:
                    self._write_to_file(DEF_OUTPUT_FILEPATH, output)
                except Exception as exc:
                    print_error(f"Unable to save output")

    @staticmethod
    def _write_to_file(filepath: str, output):
        with open(filepath, "w") as f:
            f.write(output)

    def _prepare_names(self) -> Set[str]:
        prepared = set()
        for name in self._names_raw:
            if not self._dont_capitalize:
                prepared.add(name.capitalize())
                prepared.add(self.decapitalize_str(name))
            else:
                prepared.add(name)
        return prepared

    def _prepare_dates(self) -> Set[str]:
        prepared = set()
        for date in self._dates_raw:
            if date:
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
    try:
        # x = PassGenerator(separate_input("bayan bill"),
        #                   separate_input("30.01.1980"),
        #                   separate_input("12"),
        #                   separate_input("georgia"),
        #                   separate_input("narnia"),
        #                   DEF_PASS_LEN_MIN,
        #                   DEF_PASS_LEN_MAX,
        #                   "-.",
        #                   DEF_OUTPUT_FILEPATH,
        #                   DEF_MIN_DIGITS,
        #                   DEF_MIN_UPPERS,
        #                   DEF_MIN_LOWERS,
        #                   DEF_MIN_SPECIALS,
        #                   DEF_NO_CAPITALIZATION)
        # x.generate_wordlist()
        # exit(0)

        print(f"\n{BANNER}\n"
              f"Make sure of the following:\n"
              f"1. Disregard capital letters (at the beginning of words)\n"  # todo at the vs in the
              f"2. Write two-letter words as two words (i.e \"new york\")\n"
              f"Written by {BOLD}@flashnuke{RESET}")
        print(DELIM)

        pargs = define_args()

        print_info(f"{BOLD}When providing several words, separate them using a whitespace{RESET}")
        names_input = input_validator("Enter meaningful names (i.e: First/Last names, nickname, pet name, etc):")
        dates_input = input_validator("Enter meaningful dates [DAY.MONTH.YEAR] (i.e: 24.02.2002, 31.03, etc):",
                                      "Invalid datetime format. Please use the following format:"
                                      f" {BOLD}\"%d.%m\"{RESET} or {BOLD}\"%d.%m.%Y\"{RESET}",
                                      verify_dates_input)
        numbers_input = input_validator("Enter meaningful numbers (from username, current year, etc):",
                                        "Invalid number format. Please enter digits only or nothing",
                                        verify_numbers_input)
        locations_input = input_validator("Enter meaningful locations (city of birth, residence, etc):")
        additional_input = input_validator("Enter misc words (any word you think might be of help and did not fit above):")

        x = PassGenerator(names_input, dates_input, numbers_input, locations_input, additional_input, pargs.pass_minlen,
                          pargs.pass_maxlen,
                          pargs.word_sep, pargs.output_path, pargs.min_digits, pargs.min_uppers, pargs.min_lowers,
                          pargs.min_specials, pargs.no_capitalization)
        x.generate_wordlist()

        # todo info about computation time in readme

    except KeyboardInterrupt:
        print_error("Aborted by user (CTRL+C)")
    except Exception as exc:
        print_error(f"{exc} exception occurred: {traceback.format_exc()}")
    finally:
        exit()
