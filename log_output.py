import datetime
from connection import sheet
from datafetch import data

id_dict = data()

data = sheet.sheet1.get_all_values()

third_sheet = sheet.get_worksheet(2)
running_time_data = third_sheet.get_all_values()
running_time_data.pop(0)
alpha_id = [running_total_entry[1] for running_total_entry in running_time_data]


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

    sheet.sheet1.update(f"E{index + 1}:F{index + 1}", [data[index][4:]])

    if student_id not in alpha_id:
        running_time_data.append([id_dict[student_id], student_id, 0])
        alpha_id.append(student_id)
        third_sheet.update(f"A{alpha_id.index(student_id)+2}:C{alpha_id.index(student_id)+2}",
                           [[id_dict[student_id], student_id, 0]])

    row = alpha_id.index(student_id)
    total_time = (float(running_time_data[row][2]) + time_difference)
    running_time_data[row][2] = total_time
    third_sheet.update(f"C{row + 2}", [[total_time]])

    checkout_name = id_dict[student_id]
    print(f"Checking out {checkout_name}")
# def checkout1(student_id: str, time: str, row: int):
#     """
#     checks out a student and updates the local list and gsheet (log and running time) accordingly.
#     :param student_id: the id of the student that is checking out
#     :param time: the time when they checked out
#     :param row: index at which the entry is in the list
#     """
#     checkout_name = id_dict[student_id]
#     update_total_time(student_id, row, time)
#     print(f"Checking out {checkout_name}")
#     # data[row] = [checkout_name, data[row][1], data[row][2], data[row][3], time, update_total_time(row, time)]
#     # sheet.sheet1.update(f"A{row+1}:F{row+1}", [data[row]])
#     # total_time = (float(running_time_data[alpha_id.index(student_id)][2]) + update_total_time(row, time))
#     # running_time_data[alpha_id.index(student_id)][2] = total_time
#     # third_sheet.update(f"C{(alpha_id.index(student_id))+2}", [[total_time]])


def add_time(student_id: str):
    """
    adds the entry itself to the local list and the gsheet.
    :param student_id: the id of the student that is being logged
    """
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

    for entry in data:
        if entry[4] == '':
            checkout(entry[1], data.index(entry), "18:00:00.00", True)

            # entry[4] = "00:00:00.00"
            # entry[5] = time_difference
            #
            # row = data.index(entry)+1
            # sheet.sheet1.update(f"E{row}:F{row}", [[entry[4], entry[5]]])
            # total_time = (float(running_time_data[alpha_id.index(entry[1])][2]) + entry[5])
            # running_time_data[alpha_id.index(entry[1])][2] = total_time
            # third_sheet.update(f"C{(alpha_id.index(entry[1])) + 2}", [[total_time]])
