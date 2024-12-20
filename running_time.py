from connection import sheet
from log_output import data as entries

running_time_data = sheet.sheet3.get_all_values()


for entry in entries:
    print(entry)
