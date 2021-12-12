### UTLS #######

import re 
import time 
from itertools import product 
from typing import List



def get_hour(t, output='hour'):
    h, m =map(int, time.strftime("%H %M", t).split(' '))
    if output == 'hour':
        if m >= 59:
            h += 1
        return h
    return h, m 


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

def generate_combinations(a: List[list]):
    ''' a: [[1,2], [3,4], [5,6]]
        returns: all cominations
    '''
    return list(product(*a))


def find_numerical_inputs(line):
    # (?:[eE][+-]?\d+)? optional 1e2343
    return re.findall(r"(?:\d+(?:\.\d*)?|\.\d+)(?:am|pm)?", line)


if __name__ == '__main__':
    pass # moved to unit test
    # res = convert_to_datetime("5am")
    # assert time.strftime("%H:%M:%S", res) == '05:00:00',  print('error in time conversion')
    # hour, minute = map(int, time.strftime("%H,%M", res).split(','))
