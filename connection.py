import gspread
from google.oauth2.service_account import Credentials
import pypyodbc as odbc

DRIVER_NAME = "ODBC Driver 18 for SQL Server"
SERVER_NAME = "I46061L52295744\AXIOMSQL"
DATABASE_NAME = "TestTimesheet"

connection = f"""
    DRIVER={{{DRIVER_NAME}}};
    SERVER={SERVER_NAME};
    DATABASE={DATABASE_NAME};
    Trust_Connection=yes;
"""

conn = odbc.connect(connection)
print(conn)

scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

cred = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(cred)

sheets_id = "1rzZ0NeR_ETB4F2hoxuZZb2ELTq36oKg0j3UZ3MTb-3Y"
sheet = client.open_by_key(sheets_id)
