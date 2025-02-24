from fastapi import APIRouter, UploadFile, File, Form, Request
import shutil
from typing import List

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse

upload_router = APIRouter(
    tags=["Upload"])

upload_router.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@upload_router.get("/upload", response_class=HTMLResponse)
async def upload_page(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})


@upload_router.post("/upload")
async def upload_images(files: List[UploadFile] = File(...)):
    for file in files:
        with open(file.filename, 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)
    return {"filename": [file.filename for file in files]}
