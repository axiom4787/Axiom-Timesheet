import datetime
from connection import sheet
from datafetch import data
import sys

room = sys.argv[1]

if room == "cs":
    sheet_id = 0
elif room == "mech":
    sheet_id = 1
else:
    print("retry!")
    sheet_id = 0

id_dict = data()

worksheet = sheet.get_worksheet(sheet_id)
data = worksheet.get_all_values()


def checkin(student_id: str, date: str, time: str):
    """
    Checks in a student into the timesheet log and updates it in both local list and gsheet.
    :param student_id: id of the student
    :param date: the date of the entry
    :param time: the time of the entry
    """
    checkin_name = id_dict[student_id]
    print(f"Checking in {checkin_name}")
    data.append([checkin_name, student_id, date, time, '', ''])
    row = data.index([checkin_name, student_id, date, time, '', '']) + 1
    worksheet.update(f"A{row}:D{row}", [[checkin_name, student_id, date, time]])


def checkout(student_id: str, index: int, final_time: str, auto_checkout=False):
    """
    calculates the total time a student has spent and updates it in both local list and gsheet.
    :param student_id:
    :param auto_checkout:
    :param index: the index of the entry that is being checked out
    :param final_time: time_out
    """
    time1 = datetime.datetime.strptime(data[index][3], '%H:%M:%S.%f')
    time2 = datetime.datetime.strptime(final_time, '%H:%M:%S.%f')
    time_difference = (time2 - time1).total_seconds()

    if auto_checkout:
        time_difference = round(time_difference / (3600*2), 2)
        data[index][4] = "00:00:00.00"
    else:
        time_difference = round(time_difference / 3600, 2)
        data[index][4] = final_time

    data[index][5] = time_difference

    worksheet.update(f"E{index + 1}:F{index + 1}", [data[index][4:]])

    checkout_name = id_dict[student_id]
    print(f"Checking out {checkout_name}")


def add_time(student_id: str):
    """
    adds the entry itself to the local list and the gsheet.
    :param student_id: the id of the student that is being logged
    """
    data = worksheet.get_all_values()

    current_time = str(datetime.datetime.now().time())
    current_date = str(datetime.datetime.now().date())

    for index in range(len(data)-1, -1, -1):
        if student_id == data[index][1]:
            # checking if the time out cell is empty or not
            if data[index][4] == '':
                checkout(student_id, index, current_time)
                return f"You're all set, {id_dict[student_id]}!"
            else:
                checkin(student_id, current_date, current_time)
                return f"Welcome, {id_dict[student_id]}!"
    checkin(student_id, current_date, current_time)
    return f"Welcome, {id_dict[student_id]}!"


def forgot_checkout():
    # TODO: add an auto email functionality
    """
    finds missing checkouts and fills them in with half the time from check-in to 6 pm in both the gsheet and local.
    """
    data = worksheet.get_all_values()
    for entry in data:
        if entry[4] == '':
            checkout(entry[1], data.index(entry), "18:00:00.00", True)
