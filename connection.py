import gspread
from google.oauth2.service_account import Credentials

scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

cred = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(cred)

sheets_id = "1rzZ0NeR_ETB4F2hoxuZZb2ELTq36oKg0j3UZ3MTb-3Y"
sheet = client.open_by_key(sheets_id)
sheet2 = sheet.get_worksheet(1)