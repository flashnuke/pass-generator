import argparse

DEF_PASS_LEN_MIN = 8
DEF_PASS_LEN_MAX = 32

DEF_MIN_DIGITS = 0
DEF_MIN_UPPERS = 0
DEF_MIN_LOWERS = 0
DEF_MIN_SPECIALS = 0

DEF_WORD_SEPARATORS = "_@.-"
DEF_OUTPUT_FILEPATH = "./results.txt"


def define_args():
    parser = argparse.ArgumentParser(description='A program designed to generate a password list'
                                                 ' (for dictionary-attacks) using words provided by the user')
    parser.add_argument("-m", "--min-len", dest='pass_minlen', type=int, metavar=(""), default=DEF_PASS_LEN_MIN,
                        help=f"minimum pass length (default -> {DEF_PASS_LEN_MIN})",
                        required=False)
    parser.add_argument("-x", "--max-len", dest='pass_maxlen', type=int, metavar=(""), default=DEF_PASS_LEN_MAX,
                        help=f"maximum pass length (default -> {DEF_PASS_LEN_MAX})",
                        required=False)
    parser.add_argument("--min-digits", dest='min_digits', type=int, metavar=(""), default=DEF_MIN_DIGITS,
                        help=f"minimum number of digits, passwords with below that will be omitted (default -> {DEF_MIN_DIGITS})",
                        required=False)
    parser.add_argument("--min-uppers", dest='min_uppers', type=int, metavar=(""), default=DEF_MIN_UPPERS,
                        help=f"minimum number of uppercase characters, passwords with below that will be omitted (default -> {DEF_MIN_UPPERS})",
                        required=False)
    parser.add_argument("--min-lowers", dest='min_lowers', type=int, metavar=(""), default=DEF_MIN_LOWERS,
                        help=f"minimum number of lowercase characters, passwords with below that will be omitted (default -> {DEF_MIN_LOWERS})",
                        required=False)
    parser.add_argument("--min-specials", dest='min_specials', type=int, metavar=(""), default=DEF_MIN_SPECIALS,
                        help=f"minimum number of special characters, passwords with below that will be omitted (default -> {DEF_MIN_SPECIALS})",
                        required=False)
    parser.add_argument("-s", "--seperators", dest='word_sep', type=str, metavar=(""), default=DEF_WORD_SEPARATORS,
                        help=f"word separators for password generation (default -> {DEF_WORD_SEPARATORS})",
                        required=False)
    parser.add_argument("-o", "--output", dest='output_path', type=str, metavar=(""), default=DEF_OUTPUT_FILEPATH,
                        help=f"output filepath where wordlist will be saved (default -> {DEF_OUTPUT_FILEPATH})",
                        required=False)

    return parser.parse_args()
