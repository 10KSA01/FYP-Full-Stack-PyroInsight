import pandas as pd
from datetime import datetime
import random
import time
from clock import Clock
import csv
import os

logfile_location = 'logfile.csv'

headers = [
    "datetime",                      # 0
    "reply_status",                  # 1
    "flags",                         # 2
    "node",                          # 3
    "channel",                       # 4
    "channel_address",               # 5
    "point_category",                # 6
    "point_number",                  # 7
    "logical_point_number",          # 8
    "logical_point_zone",            # 9
    "device_type",                   # 10
    "auxiliary_point_attributes",    # 11
    "group",                         # 12
    "area_type",                     # 13
    "area_number",                   # 14
    "sector_id",                     # 15
    "loop_type",                     # 16
    "raw_identity",                  # 17
    "actual_device_type",            # 18
    "mode_and_sensitivity",          # 19
    "raw_analogue_values1",          # 20
    "raw_analogue_values2",          # 21
    "raw_analogue_values3",          # 22
    "lta_flags",                     # 23
    "raw_lta",                       # 24
    "dirtiness",                     # 25
    "units_of_measure1",             # 26
    "units_of_measure2",             # 27
    "units_of_measure3",             # 28
    "converted_value1",              # 29
    "converted_value2",              # 30
    "converted_value3",              # 31
    "instantaneous_active_state",    # 32
    "instantaneous_fault_state",     # 33
    "confirmed_active_state",        # 34
    "confirmed_fault_state",         # 35
    "acknowledged_active_state",     # 36
    "acknowledged_fault_state",      # 37
    "output_forced_mode",            # 38
    "output_unforced_state",         # 39
    "output_forced_state"            # 40
]

            #0                          #1          #2    #3  #4                        #5  #6     #7 #8 #9  #10     #11 #12 #13 #14  #15   #16     #17 #18#19#20#21#22 #23             #24 #25 #26    #27     #28        #29  #30  #31  #32    #33 #34 #35  #36  #37  #38     #39     #40
device1 = ["Wed Apr 19 13:42:22 2023",	"Success", "None", 0, "MP CPU/Software Channel", 0,	"None",	1, 1, 0, "850 PH", 3, 0, 103, 103, 164, "Thorn", 41, 0,	0, 0, 0, 0,	"LTA Available", 0,	8, "None", "None", "Invalid", 116, 105, 111, "None", 95, 99, 104, 97, 110, "None", "None", "None"]

def file_exist():
    # Check if logfile exist, if it does not then write header
    if not os.path.exists(logfile_location):
        with open(logfile_location, 'a', newline='') as file:
        # Create a CSV writer
            csv_writer = csv.writer(file)
            # Write the new row to the CSV file
            csv_writer.writerow(headers)

def current_time():
    # Get the current date and time
    current_datetime = datetime.now()

    # Format the current datetime as a string in the desired format
    return current_datetime.strftime("%a %b %d %H:%M:%S %Y")



counter = 1

def get_counter():
    return counter

def set_counter(counter):
    counter = counter

## Random failures ##
def rand_failure_reply_status():
    return random.randint(4,7)

def rand_failure_flags():
    return random.randint(90,110)

def rand_failure_instantaneous_fault_state():
    return random.randint(1,255)

def rand_failure_confirmed_fault_state():
    return random.randint(1,255)

def rand_failure_acknowledged_fault_state():
    return random.randint(1,255)

def rand_failures():
    if get_counter() % rand_failure_reply_status() == 0:
        device1[1] = "Failure"

    if get_counter() % rand_failure_flags() == 0:
        device1[2] = "Loop Fault"

    if get_counter() % rand_failure_instantaneous_fault_state() == 0:
        device1[33] = str(rand_failure_instantaneous_fault_state())

    if get_counter() % rand_failure_confirmed_fault_state() == 0:
        device1[35] = str(rand_failure_confirmed_fault_state())

    if get_counter() % rand_failure_acknowledged_fault_state() == 0:
        device1[37] = str(rand_failure_acknowledged_fault_state())

def rand_dirtiness():
    return random.randint(1,100)


def update_dirtiness():
    # can change rand_num to any number between 1-100, so if rand_dirtiness() is equal to rand_num then increase the dirtiness
    rand_num = 50 
    if int(device1[25]) < 255:
        if rand_dirtiness() == rand_num:
            device1[25] = str(int(device1[25]) + 1)

def update_device():
    device1[0] = current_time()
    rand_failures()
    update_dirtiness()
    set_counter(get_counter() + 1)

    print(device1)
    with open(logfile_location, 'a', newline='') as file:
    # Create a CSV writer
        csv_writer = csv.writer(file)

        # Write the new row to the CSV file
        csv_writer.writerow(device1)

clock = Clock(start=True)
while True:
    if clock.time_elapsed(5):
        file_exist()
        print("device added")
        update_device()
    
    
    

print(device1)

print(headers)




def load_configuration():
    print("config")

def load_settings():
    print("settings")

def simulate():
    
    print("simulate")
