import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path
from core.config import settings




credentials_file = Path.cwd() / "credentials.json"
spreadsheet_id = settings.google_sheets.table_id
noyabrsk = settings.google_sheets.sheet_noyabrsk

# Объект авторизации
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
client = gspread.authorize(credentials)
spreadsheet = client.open_by_key(spreadsheet_id)
sheet = spreadsheet.worksheet(noyabrsk)
data = sheet.get(pad_values=True)
print(len(data))
print(len(data[0]))
for row in data:
    print(row)
    print(len(row))
