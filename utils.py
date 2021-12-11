### UTLS #######

import re 
import time 


def convert_to_datetime(mystr):
    for fn in ["%I%p", "%I.%M%p"]:
        try:
            result = time.strptime(mystr, fn) 
            #parse a string representing a time according to format: 0-12 hour, am or pm 
            return result
        except:
            continue 
    return False 

def split_lines(text):
    lines = re.split('(?<=\.)\s|;\s+', text)
    return lines


def find_numerical_inputs(line):
    # (?:[eE][+-]?\d+)? optional 1e2343
    return re.findall(r"(?:\d+(?:\.\d*)?|\.\d+)(?:am|pm)?", line)


if __name__ == '__main__':
    pass # moved to unit test
    # res = convert_to_datetime("5am")
    # assert time.strftime("%H:%M:%S", res) == '05:00:00',  print('error in time conversion')
