import gspread
from google.oauth2.service_account import Credentials
import datetime
import settings
import warnings

scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

cred = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(cred)

try:
    sheets_id = settings.load("sheets_id")
except FileNotFoundError:
    warnings.warn("SHEET ID NOT FOUND. USING DEFAULT SHEET ID")
    sheets_id = "1rzZ0NeR_ETB4F2hoxuZZb2ELTq36oKg0j3UZ3MTb-3Y"

sheet = client.open_by_key(sheets_id)
