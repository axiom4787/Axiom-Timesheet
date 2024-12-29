# import base64
# from google.oauth2.service_account import Credentials
# from googleapiclient.discovery import build
# from email.mime.text import MIMEText
# from connection import sheet
#
# SCOPES = ['https://mail.google.com/']
# creds = Credentials.from_service_account_file('gmail_credentials.json', scopes=SCOPES)
#
# service = build('gmail', 'v1', credentials=creds)
#
# data = sheet.get_worksheet(1).get_all_values()
# email_dict = {row[3]: row[1] for row in data[1:]}
#
#
# def send_email(to_id, subject, message_text):
#     message = MIMEText(message_text)
#     # message['to'] = email_dict[to_id]
#     message['to'] = "mail2tanmaygarg@gmail.com"
#     message['subject'] = subject
#     raw = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
#     send_message = {'raw': raw}
#     print(message)
#     try:
#         sent_message = service.users().messages().send(userId='axiomtimesheet@axiom-timesheet.iam.gserviceaccount.com',
#                                                        body=send_message).execute()
#         print(f"Message sent successfully: {sent_message['id']}")
#     except Exception as error:
#         print(f"An error occurred: {error}")

import smtplib
from email.mime.text import MIMEText
import os
password = os.environ.get("EMAIL_PASSWORD")


def send_email(to_id, message_text):
    """
    Sends an email to the given email address with the given subject and message.
    :param to_id: the email address of the recipient
    :param subject: the subject of the email
    :param message_text: the message to be sent
    """
    sender = "axiom.scout.4787@gmail.com"
    message = MIMEText(message_text)
    recipient = "mail2tanmaygarg@gmail.com"
    message['to'] = "mail2tanmaygarg@gmail.com"
    message['subject'] = "Forgot to Check Out"
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp_server:
        smtp_server.starttls()
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipient, message.as_string())
