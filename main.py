from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from typing import Optional, List
from collections import defaultdict 

import pydantic
from pydantic import parse_obj_as, validator

from time import sleep
import datetime 
import re
from pprint import pprint
from utils import * 


browser = webdriver.Chrome(executable_path='./drivers/chromedriver')

#a single validator can also be called on all fields by passing the special value '*'


class MALL(pydantic.BaseModel):
    car_park : str
    weekday: str
    saturday: str
    sunday: str

    def __init__(self, *args):
        # do some manipulation before callingn super()
        b5 = args[1] + '; ' + args[2]

        super().__init__(car_park=args[0],
                        weekday=b5,
                        saturday=args[3],
                        sunday=args[4]
        )


    @validator('saturday', 'sunday')
    def check_same_as_weekend(cls, v, values):
        if v.lower() == 'same as weekdays':
            print('in validator ', values['weekday'])
            return values['weekday']
        elif v.lower() == 'same as saturday':
            print('in validator sat: ', values['saturday'])
            return values['saturday']
        return v


    @validator('*', pre=True)
    def check_for_special_char(cls, v):
        assert isinstance(v, str)
        if '½ hr' in v:
            v = v.replace('½ hr', '30 mins')
            print('in validator ½ hr', v)
        if 'sub.' in v:
            v = v.replace('sub.', 'sub')
            print('in validator sub.')
        if 'hr;' in v:
            v = v.replace('hr;', 'hr,')
        return v




class ParkingHour(pydantic.BaseModel):
    p_type : str # per-entry, base+sub
    start_hour: Optional[time.struct_time] = None # some fields does not have this info
    end_hour:  Optional[time.struct_time] = None 
    base_rate: float  # can be base rate or per entry
    sub_rate: Optional[float] = 0.0





class PROC_MALL:
    def __init__(self, mall: MALL):
        self.car_park = mall.car_park 
        self.weekday = self.get_info(mall.weekday) #List[ParkingHour]
        self.saturday = self.get_info(mall.saturday)
        self.sunday = self.get_info(mall.sunday)

    def get_info(self, data):
        wd_parking = [] # whole day parking

        #lines: List[str] = re.split("\s?mins(?:.)?", data)
        lines = split_lines(data)
        for line in lines:
            # get the time, parking rate
            if re.search("[0-9]+(am|pm).*[0-9]+(am|pm)(?:.+)?[0-9]+.*[0-9]+(?:.+)?hr.*[0-9]+(?:.+)?for sub(?:.+)?[0-9]+(mins|min)?", line):
                '''base + sub rate'''
                result = find_numerical_inputs(line) 
                if len(result) != 6:
                    continue 
                print(f"{line} base+sub rate: {result}, {len(result)} \n")
                input_dat = {
                    'p_type': 'base_sub',
                    'start_hour': convert_to_datetime(result[0]),
                    'end_hour': convert_to_datetime(result[1]),
                    'base_rate': float(result[2]), 
                    'sub_rate': float(result[3])
                }
                wd_parking.append( ParkingHour(**input_dat) )
            elif re.search("[0-9]+(am|pm).*[0-9]+(am|pm)(?:.+)?[0-9]+.*entry(?:.)?$", line):
                ''' per entry with time'''
                result = find_numerical_inputs(line) 
                print(f"{line} per entry: {result}, {len(result)} \n")
                input_dat = {
                    'p_type': 'per_entry_with_time',
                    'start_hour': convert_to_datetime(result[0]),
                    'end_hour': convert_to_datetime(result[1]),
                    'base_rate': float(result[2]), 
                    'sub_rate': 0.0,
                }
                wd_parking.append( ParkingHour(**input_dat))
            elif re.search("[0-9]+(am|pm).*per entry(?:.)?",  line ):
                ''' per entry after time'''
                result = find_numerical_inputs(line)
                print(f"{line} per entry aft hour: {result}, {len(result)} \n")
                input_dat = {
                    'p_type': 'per_entry_after_hour',
                    'start_hour': convert_to_datetime(result[0]),
                    'end_hour': convert_to_datetime("11:59pm"),
                    'base_rate': float(result[1]), 
                    'sub_rate': 0.0,
                }
                wd_parking.append( ParkingHour(**input_dat) )
            elif re.search("[0-9]+\s+per entry", line):
                result = find_numerical_inputs(line)
                print(f"{line} PER_ENTRY: {result}, {len(result)} \n")
                input_dat = {
                    'p_type': 'per_entry',
                    'start_hour': None,
                    'end_hour': None,
                    'base_rate': float(result[0]),
                    'sub_rate': 0.0,
                }
                wd_parking.append( ParkingHour(**input_dat) )
            else:
                print('empty line? ', line, self.car_park)

        return wd_parking 


URL = "https://onemotoring.lta.gov.sg/content/onemotoring/home/owning/ongoing-car-costs/parking/parking_rates.1.html"

browser.get(URL)

nameList = browser.find_elements_by_css_selector('table.parking_rate tr')

mall_list = []


counter = 0
for row in nameList:
    #print(name.text)
    if counter == 4:
        break
    counter += 1

    col_list = []
    cols = row.find_elements_by_tag_name('td')
    if not cols:
        continue 

    for col in cols:
        print(col.text)
        col_list.append(col.text)
    print(" ------------")
    mall_list.append(col_list)

browser.quit()



#print(mall_list)
assert len(mall_list[0]) == 5

malls: List[MALL]  = [ MALL(*mall) for mall in mall_list ]



#pprint(malls)


print('---- proc mall --------\n')

proc_malls: List[PROC_MALL]  = [ PROC_MALL(mall) for mall in malls]

[ pprint(pm.__dict__) for pm in proc_malls ]