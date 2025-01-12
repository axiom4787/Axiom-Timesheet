import datetime
import hashlib

from connection import sheet
from datafetch import data
import sys

import threading
from datetime import datetime
import boto3
import os

room = sys.argv[1]

if room == "cs":
    sheet_id = 1
elif room == "mech":
    sheet_id = 2
elif room == "queue":
    sheet_id = 5
else:
    print("retry!")
    sheet_id = 0

id_dict = data()

worksheet = sheet.get_worksheet(sheet_id)
data = worksheet.get_all_values()


sqs = boto3.resource('sqs')
queue_url = os.getenv("QUEUE_URL")
entry_queue = sqs.Queue(queue_url)


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
    time1 = datetime.strptime(data[index][3], '%H:%M:%S.%f')
    time2 = datetime.strptime(final_time, '%H:%M:%S.%f')
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


def add_time(student_id: str, datestamp, timestamp):
    """
    adds the entry itself to the local list and the gsheet.
    :param student_id: the id of the student that is being logged
    """
    data = worksheet.get_all_values()

    current_time = str(timestamp)
    current_date = str(datestamp)

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


def send(student_id):
    current_date = str(datetime.now().date())
    current_time = str(datetime.now().time())
    text = f"{student_id}, {current_date}, {current_time}"
    entry_queue.send_message(MessageBody=text,
                             MessageGroupId='default',
                             MessageDeduplicationId=hashlib.md5(text.encode()).hexdigest()
                             )


def receive():
    while True:
        for message in entry_queue.receive_messages():
            task = message.body.split(", ")
            student_id = task[0]
            date = task[1]
            time = task[2]
            add_time(student_id, date, time)
            message.delete()


receiving_thread = threading.Thread(target=receive, daemon=True)
receiving_thread.start()
