import pandas as pd
from datetime import datetime
import random
from clock import Clock
import csv
import json
import os

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

class FakeDeviceSimulator:
    def __init__(self):
        self.load_config()
        self.devices = pd.DataFrame()
        
    def find_config(self):
        # Get the current directory
        current_directory = os.path.dirname(os.path.abspath(__file__))
        # Construct the file path to config.json
        config_file_path = os.path.join(current_directory, 'config.json')

        return config_file_path
    
    def load_config(self):
        with open(self.find_config(), 'r') as config_file:
            config_data = json.load(config_file)
        
        self.find_log_file_path = config_data["find_log_file_path"]
        self.find_devices_file_path = config_data["find_devices_file_path"]
        self.counter = config_data["counter"]
        
        return self
        
    def logfile_exist(self):
        print("Checking if file exist \n")
        # Check if logfile exist, if it does not then write header
        if not os.path.exists(self.find_log_file_path):
            with open(self.find_log_file_path, 'a', newline='') as file:
            # Create a CSV writer
                csv_writer = csv.writer(file)
                # Write the new row to the CSV file
                csv_writer.writerow(headers)
    
    def load_devices(self):
        print("Loading Devices\n") 
        # read csv file into DataFrame
        self.devices = pd.read_csv(self.find_devices_file_path)
                
    def current_time(self):
        # Get the current date and time
        current_datetime = datetime.now()
        # Format the current datetime as a string in the desired format
        return current_datetime.strftime("%a %b %d %H:%M:%S %Y")

    def get_counter(self):
        return self.counter

    def set_counter(self, new_counter):
        self.counter = new_counter

    def save_counter(self):
        with open(self.find_config(), 'r') as config_file:
            config_data = json.load(config_file)
        
        # Update the "counter" value in the JSON data     
        config_data["counter"] = self.get_counter()
        
        # Write the updated JSON data back to the config.json file
        with open(self.find_config(), 'w') as config_file:
            config_file.write(json.dumps(config_data, indent=4))

    ## Random failures ##
    def rand_failure_reply_status(self):
        return random.randint(4,7)

    def rand_failure_flags(self):
        return random.randint(90,110)

    def rand_failure_instantaneous_fault_state(self):
        return random.randint(1,255)

    def rand_failure_confirmed_fault_state(self):
        return random.randint(1,255)

    def rand_failure_acknowledged_fault_state(self):
        return random.randint(1,255)

    def rand_failures(self, index):
        if self.get_counter() % self.rand_failure_reply_status() == 0:
            self.devices.iloc[index, 1] = "Failure"

        if self.get_counter() % self.rand_failure_flags() == 0:
            self.devices.iloc[index, 2] = "Loop Fault"

        if self.get_counter() % self.rand_failure_instantaneous_fault_state() == 0:
            self.devices.iloc[index, 33] = str(self.rand_failure_instantaneous_fault_state())

        if self.get_counter() % self.rand_failure_confirmed_fault_state() == 0:
            self.devices.iloc[index, 35] = str(self.rand_failure_confirmed_fault_state())

        if self.get_counter() % self.rand_failure_acknowledged_fault_state() == 0:
            self.devices.iloc[index, 37] = str(self.rand_failure_acknowledged_fault_state())

    def rand_hundred(self):
        return random.randint(1,101)
    
    def rand_ten(self):
        return random.randint(1,11)

    def update_dirtiness(self, index):
        # can change rand_num to any number between 1-100, so if rand_dirtiness() is equal to rand_num then increase the dirtiness
        rand_num = 50
        dev_dirtiness = self.devices.iloc[index, 25] 
        if int(dev_dirtiness) < 255:
            if self.rand_hundred() == rand_num:
                dev_dirtiness = str(int(dev_dirtiness) + 1)
    
    def check_device_type(self, index):
        device_type = self.devices.iloc[index, 10].split()
        return device_type[1]
    
    def update_type_value(self, index):
        rand_num = 5
        value1 = ""
        value2 = ""

        if self.check_device_type(index) == "H":
            value1 = self.devices.iloc[index, 29]
        elif self.check_device_type(index) == "P":
            value1 = self.devices.iloc[index, 29]
        elif self.check_device_type(index) == "PC":
            value1 = self.devices.iloc[index, 30] 
        elif self.check_device_type(index) == "PH":
            value1 = self.devices.iloc[index, 31]

        if int(value1) < 255:
            if self.rand_ten() == rand_num:
                if int(value1) > 0:
                    if random.choice([True, False]) == True:
                        value1 = str(int(value1) + 1)
                    else:
                        value1 = str(int(value1) + 1)
        
        if self.check_device_type(index) == "H":
            value = self.devices.iloc[index, 29]
        elif self.check_device_type(index) == "PC":
            value = self.devices.iloc[index, 30] 
        elif self.check_device_type(index) == "PH":
            value = self.devices.iloc[index, 31]

    def update_device(self):
        for index, device in self.devices.iterrows():
            self.devices.iloc[index, 0] = self.current_time()
            self.rand_failures(index)
            self.update_dirtiness(index)
            self.update_type_value(index)
            
            self.set_counter(self.get_counter() + 1)

            with open(self.find_log_file_path, 'a', newline='') as file:
            # Create a CSV writer
                csv_writer = csv.writer(file)

                # Write the new row to the CSV file
                csv_writer.writerow(device)

            self.devices.to_csv(self.find_devices_file_path, index=False)
            
        print("Devices simulated \n")

def main():
    clock = Clock(start=True)
    simulator = FakeDeviceSimulator()
    simulator.load_devices()
    simulator.logfile_exist()
    simulator.update_device()
    while True:
        if clock.time_elapsed(60):
            simulator.load_devices()
            simulator.update_device()
            print(simulator.get_counter())
        
if __name__ == "__main__":
    main()
    
