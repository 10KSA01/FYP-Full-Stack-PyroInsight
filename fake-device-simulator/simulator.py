import pandas as pd
from datetime import datetime
import random
import time
from clock import Clock
# Get the current date and time
current_datetime = datetime.now()

# Format the current datetime as a string in the desired format
formatted_datetime = current_datetime.strftime("%a %b %d %H:%M:%S %Y")

counter = 0

# Display the DataFrame
print(formatted_datetime)



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

print(device1)
def rand_failure_reply_status():
    return random.randint(4,7)

def rand_failure_flags():
    return random.randint(90,110)
def update_device():
    device1[0] = formatted_datetime
    if counter % rand_failure_reply_status == 0:
        device1[1] = "Failure"
    if counter % rand_failure_flags == 0:
        device1[1] = "Loop Fault"
while True:
    print("Start")
    clock = Clock(start=True)
    if clock.time_elapsed(5):
        update_device()
        

    
    
    

print(device1)

print(headers)




def load_configuration():
    print("config")

def load_settings():
    print("settings")

def simulate():
    
    print("simulate")
