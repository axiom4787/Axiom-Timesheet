import datetime
from connection import sheet

data = sheet.sheet1.get_all_values()

names = []
for person in data:
    names.append(person[0])


def checkin(name, time):
    print(f"Checking in {name}")
    data.append([name, time, '', ''])
    row = data.index([name, time, '', '']) + 1
    sheet.sheet1.update(f"A{row}:B{row}", [[name, time]])


def checkout(name, time, row):
    print(f"Checking out {name}")
    data[row-1] = [name, data[row-1][1], time, '']
    sheet.sheet1.update(f"A{row+1}:D{row+1}", [data[row-1]])


def add_time(name):
    time = str(datetime.datetime.now())

    for index in range(len(data)-1, -1, -1):
        if name in data[index] and data[index][2] == '':
            checkout(name, time, index)
            break
        elif data[index][2] != '':
            checkin(name, time)
            break
