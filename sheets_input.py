import datetime
from connection import sheet

data = sheet.sheet1.get_all_values()

names = []
for person in data:
    names.append(person[0])


def checkin(name, date, time):
    print(f"Checking in {name}")
    data.append([name, date, time, '', ''])
    row = data.index([name, date, time, '', '']) + 1
    sheet.sheet1.update(f"A{row}:C{row}", [[name, date, time]])


def update_total_time(index):
    time_format = "%:%:%"
    time1 = datetime.datetime.strptime(data[index][2], time_format)
    time2 = datetime.datetime.strptime(data[index][3], time_format)
    time_difference = time2 - time1
    data[index][3] = time_difference
    return time_difference


def checkout(name, time, row):
    print(f"Checking out {name}")
    data[row-1] = [name, data[row-1][1], data[row-1][2], time, update_total_time(row-1)]
    sheet.sheet1.update(f"A{row+1}:E{row+1}", [data[row-1]])


def add_time(name):
    time = str(datetime.datetime.now().time())
    date = str(datetime.datetime.now().date())

    for index in range(len(data)-1, -1, -1):
        if name in data[index] and data[index][3] == '':
            checkout(name, time, index)
            break
        elif data[index][3] != '':
            checkin(name, date, time)
            break
