from connection import sheet
from log_output import data as entries

running_time_data = sheet.sheet3.get_all_values()
running_time_data.pop(0)
names = [time[0] for time in running_time_data]
running_time = {}

for name in names:
    running_time[name] = 0

for entry in entries:
    running_time[entry[0]] += entry[4]
