### UTLS #######

import re 
import time 
from itertools import product 
from typing import List




def generate_hour_list(start_hour:int, end_hour:int)-> List[int]:
    if start_hour <= end_hour:
        # 0700 -> 2000
        return list(range(start_hour, end_hour))
    else:
        # 5pm -> 7am
        # to midnight, midnight to wee hour
        return list(range(start_hour, 24)) + \
                list(range(0, end_hour))


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
    if re.search('(?:\d+(?:\.\d*)?|\.\d+)/[0-9]+(?:.*)?min(s)?.*(?:\d+(?:\.\d*)?|\.\d+)(am|pm).*(?:\d+(?:\.\d*)?|\.\d+)(am|pm)', text):
        #print("special case : e.g.$1.30/30 min  7am to 11am $1.50/30 mins 11am to 5pm")
        rate_per_x_min = re.findall("(?:\$)?(?:\d+(?:\.\d*)?|\.\d+)/[0-9]+.?min", text)
        start_to_end_hour = re.findall("(?:\d+(?:\.\d*)?|\.\d+)(?:am|pm)?\s?to\s?(?:\d+(?:\.\d*)?|\.\d+)(?:am|pm)?", text)
        lines = ["{} {}".format(b,a) for a, b in zip(rate_per_x_min, start_to_end_hour)]
        print('special split line \n', lines)
    else:
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
