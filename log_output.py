import datetime
from connection import sheet

data = sheet.sheet1.get_all_values()

names = []
for person in data:
    names.append(person[0])


def checkin(name: str, date: str, time: str):
    """
    Checks in a student into the timesheet log and updates it in both local list and gsheet.
    :param name: name of the student
    :param date: the date of the entry
    :param time: the time of the entry
    """
    print(f"Checking in {name}")
    data.append([name, date, time, '', ''])
    row = data.index([name, date, time, '', '']) + 1
    sheet.sheet1.update(f"A{row}:C{row}", [[name, date, time]])


def update_total_time(index: int, final_time: str):
    """
    calculates the total time a student has spent and updates it in both local list and gsheet.
    :param index: the index of the entry that is being checked out
    :param final_time: time_out
    :return: the difference in time-out and time-in in terms of hours in decimals
    """
    time1 = datetime.datetime.strptime(data[index][2], '%H:%M:%S.%f')
    time2 = datetime.datetime.strptime(final_time, '%H:%M:%S.%f')
    time_difference = (time2 - time1).total_seconds()
    time_difference = round(time_difference / 3600, 2)
    data[index][3] = time_difference
    return time_difference


third_sheet = sheet.get_worksheet(2)
running_time_data = third_sheet.get_all_values()
running_time_data.pop(0)
alpha_names = [running_total_entry[0] for running_total_entry in running_time_data]

for running_entry in running_time_data:
    try:
        running_entry[1] = float(running_entry[1])
    except Exception as e:
        print(e, running_entry)


def update_running_time(name: str, total_time: float):
    running_time_data[alpha_names.index(name)][1] += total_time
    return running_time_data[alpha_names.index(name)][1]


def checkout(name: str, time: str, row: int):
    """
    checks out a student and updates the local list and gsheet accordingly.
    :param name: the student that is checking out
    :param time: the time when they checked out
    :param row: index at which the entry is in the list
    """
    print(f"Checking out {name}")
    data[row] = [name, data[row][1], data[row][2], time, update_total_time(row, time)]
    sheet.sheet1.update(f"A{row+1}:E{row+1}", [data[row]])
    third_sheet.update(f"B{(alpha_names.index(name))+2}",
                        [[update_running_time(name, update_total_time(row, time))]])


def add_time(name: str):
    """
    adds the entry itself to the local list and the gsheet.
    :param name: the student that is being logged
    """
    time = str(datetime.datetime.now().time())
    date = str(datetime.datetime.now().date())

    for index in range(len(data)-1, -1, -1):
        if name in data[index] and data[index][3] == '':
            checkout(name, time, index)
            break
        elif data[index][3] != '':
            checkin(name, date, time)
            break
