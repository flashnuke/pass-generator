import argparse

DEF_PASS_LEN_MIN = 8
DEF_PASS_LEN_MAX = 32
DEF_WORD_SEPARATORS = "_@.-"
DEF_OUTPUT_FILEPATH = "./results.txt"


def define_args():
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
    parser.add_argument("-o", "--output", dest='output_path', type=str, metavar=(""), default=DEF_WORD_SEPARATORS,
                        help=f"output filepath where wordlist will be saved (default -> {DEF_OUTPUT_FILEPATH})",
                        required=False)

    return parser.parse_args()
