![image_2024-03-25_14-28-54](https://github.com/flashnuke/pass-generator/assets/59119926/98b48a1b-3238-4ded-b6a7-7740605c81e4)

</br>
A tool used to generate a wordlist from user input, in order to use for password dictionary attacks

## How it works
<img width="720" src="https://github.com/flashnuke/pass-generator/assets/59119926/061c39c1-f14c-403b-ad57-d44979e01149">

1. The program promts the user for input (words, numbers, dates...)
2. Generates a wordlist out of all subsets inside the powerset, using different separators and text manipulation
3. Filters out irrelevant passwords (long / short ones, etc)
4. Saves result into an output file

# Usage
```bash
python3 pass-generator.py
```

### Usage notes
*  Password properties can be set using cmdline arguments, run `python3 pass-generator.py -h` for more details
*  The time complexity of adding an additional word (assuming its capitalized/uncapitalized version is not added is $O(2^n)$, if generation time takes too long consider passing less separators (`-s`) or using less words

# Disclaimer

This tool is only for testing and can only be used where strict consent has been given. Do not use it for illegal purposes! It is the end user’s responsibility to obey all applicable local, state and federal laws. I assume no liability and am not responsible for any misuse or damage caused by this tool and software.

Distributed under the GNU License.
