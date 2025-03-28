import gspread
from oauth2client.service_account import ServiceAccountCredentials
from core.config import settings
from fastapi import APIRouter

credentials_file = settings.googlesheets.credentialspath
spreadsheet_id = settings.googlesheets.tableid
noyabrsk = settings.googlesheets.noyabrsk
ugansk = settings.googlesheets.ugansk

# Объект авторизации
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
client = gspread.authorize(credentials)
spreadsheet = client.open_by_key(spreadsheet_id)


def get_noyabrsk_table():
    sheet = spreadsheet.worksheet(noyabrsk)
    data = sheet.get(pad_values=True)
    return data


def get_ugansk_table():
    sheet = spreadsheet.worksheet(ugansk)
    data = sheet.get(pad_values=True)
    return data


google_sheets_router = APIRouter()


@google_sheets_router.get("/google_sheets_noyabrsk")
async def get_noyabrsk():
    return get_noyabrsk_table()


@google_sheets_router.get("/google_sheets_ugansk")
async def get_ugansk():
    return get_ugansk_table()
