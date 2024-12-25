import datetime
from connection import sheet
from datafetch import data
from auto_email import send_email

id_dict = data()

data = sheet.sheet1.get_all_values()


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
    sheet.sheet1.update(f"A{row}:D{row}", [[checkin_name, student_id, date, time]])


def update_total_time(index: int, final_time: str) -> float:
    """
    calculates the total time a student has spent and updates it in both local list and gsheet.
    :param index: the index of the entry that is being checked out
    :param final_time: time_out
    :return: the difference in time-out and time-in in terms of hours in decimals
    """
    time1 = datetime.datetime.strptime(data[index][3], '%H:%M:%S.%f')
    time2 = datetime.datetime.strptime(final_time, '%H:%M:%S.%f')
    time_difference = (time2 - time1).total_seconds()
    time_difference = round(time_difference / 3600, 2)
    data[index][5] = time_difference
    return time_difference


third_sheet = sheet.get_worksheet(2)
running_time_data = third_sheet.get_all_values()
running_time_data.pop(0)
alpha_id = [running_total_entry[1] for running_total_entry in running_time_data]


def checkout(student_id: str, time: str, row: int):
    """
    checks out a student and updates the local list and gsheet (log and running time) accordingly.
    :param student_id: the id of the student that is checking out
    :param time: the time when they checked out
    :param row: index at which the entry is in the list
    """
    checkout_name = id_dict[student_id]
    print(f"Checking out {checkout_name}")
    data[row] = [checkout_name, data[row][1], data[row][2], data[row][3], time, update_total_time(row, time)]
    sheet.sheet1.update(f"A{row+1}:F{row+1}", [data[row]])
    total_time = (float(running_time_data[alpha_id.index(student_id)][2]) + update_total_time(row, time))
    running_time_data[alpha_id.index(student_id)][2] = total_time
    third_sheet.update(f"C{(alpha_id.index(student_id))+2}", [[total_time]])


def add_time(student_id: str):
    """
    adds the entry itself to the local list and the gsheet.
    :param student_id: the id of the student that is being logged
    """
    time = str(datetime.datetime.now().time())
    date = str(datetime.datetime.now().date())

    for index in range(len(data)-1, -1, -1):
        if student_id in data[index]:
            if data[index][4] == '':
                checkout(student_id, time, index)
                return f"You're all set, {id_dict[student_id]}!"
            elif data[index][4] != '':
                checkin(student_id, date, time)
                return f"Welcome, {id_dict[student_id]}!"
    checkin(student_id, date, time)
    return f"Welcome, {id_dict[student_id]}!"


def forgot_checkout():
    # TODO: add an auto email functionality
    # TODO: add print statement for everyone who forgot to checkout
    """
    finds missing checkouts and fills them in with half the time from check-in to 6 pm in both the gsheet and local.
    """
    names_forgot = []
    for entry in data:
        if entry[4] == '':
            time1 = datetime.datetime.strptime(entry[3], '%H:%M:%S.%f')
            time2 = datetime.datetime.strptime("18:00:00.00", '%H:%M:%S.%f')
            time_difference = (time2 - time1).total_seconds()
            time_difference = round(time_difference / 3600, 2)
            time_difference = time_difference / 2

            entry[5] = time_difference
            entry[4] = "FALSE"

            row = data.index(entry)+1
            sheet.sheet1.update(f"E{row}:F{row}", [[entry[4], entry[5]]])
            total_time = (float(running_time_data[alpha_id.index(entry[1])][2]) + entry[5])
            running_time_data[alpha_id.index(entry[1])][2] = total_time
            third_sheet.update(f"C{(alpha_id.index(entry[1])) + 2}", [[total_time]])

            names_forgot.append([entry[0], entry[1]])

            subject_string = "Forgot to checkout"
            message_string = (f"Hello {entry[0]},"
                              f"\n\nYou forgot to checkout. You will receive half the time from your checkin to 6 pm."
                              f"\n\nBest, \nAxiom")
            send_email(entry[1], subject_string, message_string)

    print(f"Who forgot to checkout: {names_forgot}")
