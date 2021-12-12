from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import numpy as np 
from typing import Optional, List
from collections import defaultdict 

import pydantic
from pydantic import parse_obj_as, validator

from time import sleep
import datetime 
import re
from pprint import pprint
from utils import * 
import pandas as pd 


#https://www.stackvidhya.com/pretty-print-dataframe/
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 50)
pd.set_option('display.colheader_justify', 'center')
pd.set_option('display.precision', 1)




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
    base_rate_period: Optional[float] = None
    sub_rate: Optional[float] = None 
    sub_rate_period: Optional[float] = None 

    # def __repr__(self):
    #     return {
    #         p_type: self.p_type,
    #         start_hour: time.strftime(self.start_hour),
    #         end_hour: time.strftime(self.end_hour),
    #         base_rate: self.base_rate, 
    #         sub_rate: self.sub_rate, 
    #     }




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
                    'base_rate_period': float(result[3]),
                    'sub_rate': float(result[4]),
                    'sub_rate_period': float(result[5]), 
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
    if counter == 2:
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

## create a multiindex series


def get_mall_names(proc_malls):
    lst = [mall.car_park for mall in proc_malls]
    return lst 

def get_mall_fields(mall):
    #return [ a for a in dir(mall) if a in ['weekday', 'saturday', 'sunday']]
    for attr, value in mall.__dict__.items():
        if attr in ['weekday', 'saturday', 'sunday']:
            yield attr, value 


def populate_rates(proc_malls, df):
    print('-|'*50)
    for mall in proc_malls:
        cp_name = mall.car_park
        # iterate over different parking rate list 
        for field, value in get_mall_fields(mall):
            #(mall, field)
            # get starting hour 
            objs : List[Parking_Hour] = value
            for obj in objs: 
                print(cp_name, obj)
                assert isinstance(obj, ParkingHour)
                if obj.p_type == 'base_sub':
                    print(' BASE SUB --- ' * 5)
                    sh, eh = get_hour(obj.start_hour), get_hour(obj.end_hour)
                elif obj.p_type == 'per_entry':
                    #print(' PER ENTRY --- ' * 5)
                    sh, eh = 0, 24
                elif obj.p_type == 'per_entry_with_time':
                    #print(' PER ENTRY WITH TIME --- ' * 5)
                    sh, eh = get_hour(obj.start_hour), get_hour(obj.end_hour)
                elif obj.p_type == 'per_entry_after_time':
                    print('PER ENTRY AFTER TIME -- '* 5)
                    sh, eh = get_hour(obj.start_hour), 24
                else: 
                    print('- Error -'* 10)
                    raise NotImplementedError(f'{obj.p_type} is not implemented!')
                
                hour_list = generate_hour_list(sh, eh)
                sub_rate = obj.sub_rate if obj.sub_rate else 0.0
                print('#'*100)
                print(f"{cp_name}: writing fields: {field}, {hour_list}, {obj.base_rate}, {sub_rate} \n")
                for h in hour_list:
                    df.loc[(cp_name, field, h), :] = obj.base_rate, sub_rate 
    return 


def create_dataframe(proc_malls: List[PROC_MALL]) -> pd.DataFrame:
    
    mall_names = get_mall_names(proc_malls)
    days = ['weekday', 'saturday', 'sunday']
    time = range(24)
    col_names =['car_park', 'days', 'hour']
    comb = generate_combinations([mall_names, days, time])
    #df = pd.DataFrame(comb, columns=col_names)
    
    # create a multiindex so that values of base rate and sub rate are easier to populate
    index = pd.MultiIndex.from_product([mall_names, days, time], 
            names=col_names)
    cols = pd.MultiIndex.from_tuples(['base_rate', 'sub_rate'])
    length_of_df = len(comb)

    df = pd.DataFrame( np.zeros((length_of_df, 2))*np.nan, 
            index=index, columns=cols)
    
    populate_rates(proc_malls, df)

    base_rate = []# infer from proc object
    return df 

print('*'*100)
field = get_mall_fields(proc_malls[0])
print(field)

table = create_dataframe(proc_malls) 
table.to_csv('parking_rates.csv')



# print('*'*100)
# print(table )
# print(table.index)