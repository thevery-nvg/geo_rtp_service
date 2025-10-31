import gspread
from oauth2client.service_account import ServiceAccountCredentials
from core.config import settings
from fastapi import APIRouter
from pathlib import Path
import json
import re
from src.google_sheets.schemas import  NngDataWrite, NngDataGet

# table_spreadsheet_id = settings.googlesheets.tableid
db_spreadsheet_id= settings.googlesheets.dbtableid#"1160jfh4-hCgGcMSfMJ6tbbpUSwJFf6VjzTgxKSwjmQ4"
noyabrsk = settings.googlesheets.noyabrsk
ugansk = settings.googlesheets.ugansk

BASE_DIR = Path(__file__).parent.parent.parent
credentials_file = BASE_DIR / "src" / "google_sheets" / "credentials.json"

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

gs_router = APIRouter(
    prefix="/sheets_api",
    tags=["Api"],
)

credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
client = gspread.authorize(credentials)
db_spreadsheet = client.open_by_key(db_spreadsheet_id)
# table_spreadsheet = client.open_by_key(table_spreadsheet_id)
table=settings.googlesheets.maindbname#"main"
json_storage=BASE_DIR/"json_storage"


@gs_router.post("/write_nng_data")
async def write_nng_data(request: NngDataWrite):
    reg_number=request.passport["B17"]["value"]
    year=request.passport["B38"]["value"]
    passport=json.dumps(request.passport)
    coordinates=json.dumps(request.coordinates)
    control_places=json.dumps(request.control_places)
    valves=json.dumps(request.valves)
    sheet = db_spreadsheet.worksheet(table)
    x=sheet.find(reg_number)
    sheet.batch_get()

    if not x:
        cells=sheet.append_row([year,reg_number,passport,coordinates,control_places,valves ], table_range="A1:F1")
        p=re.compile(r"\d+$")
        str_number=re.search(p,cells["updates"]["updatedRange"]).group(0)
    else:
        sheet.update_acell(f"A{x.row}", year)
        sheet.update_acell(f"B{x.row}", reg_number)
        sheet.update_acell(f"C{x.row}", passport)
        sheet.update_acell(f"D{x.row}", coordinates)
        sheet.update_acell(f"E{x.row}", control_places)
        sheet.update_acell(f"F{x.row}", valves)
        str_number=x.row


    with open(f'{json_storage}\\{reg_number}_{year}_nng.json', 'w') as f:
        f.write(json.dumps({'passport': request.passport, 'coordinates': request.coordinates,
              'control_places': request.control_places, 'valves': request.valves}))

    return {"str_number": str_number}

@gs_router.post("/get_nng_data")
async def get_nng_data(request: NngDataGet):
    reg_number=request.reg_number
    year=request.year

    with open(f'{reg_number}_{year}_nng.json', 'r') as f:
        data = json.load(f)

    return {"data": data}