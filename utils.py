### UTLS #######

import re 
import time 


def convert_to_datetime(mystr):
    return time.strptime(mystr, "%I%p") #parse a string representing a time according to format: 0-12 hour, am or pm 


def find_numerical_inputs(line):
    # (?:[eE][+-]?\d+)? optional 1e2343
    return re.findall(r"(?:\d+(?:\.\d*)?|\.\d+)(?:am|pm)?", line)


if __name__ == '__main__':
    pass # moved to unit test
    # res = convert_to_datetime("5am")
    # assert time.strftime("%H:%M:%S", res) == '05:00:00',  print('error in time conversion')