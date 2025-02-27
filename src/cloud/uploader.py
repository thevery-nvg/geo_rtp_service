from datetime import datetime
from fastapi import APIRouter, UploadFile, File, Form, Request, Depends
import shutil
from typing import List
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse
from pathlib import Path
from auth import current_user_strict
from auth.models import User
from core.config import settings
from loguru import logger
from services import format_size

upload_router = APIRouter(
    tags=["Upload"])

upload_router.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
cloud = Path(settings.cloud.url)


@upload_router.get("/upload", response_class=HTMLResponse)
async def upload_page(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})


@upload_router.post("/upload")
async def upload_files(files: List[UploadFile] = File(...), user="Aleshka"):
    logger.info(f"{user} is uploading {len(files)} files; size = "
                f"{format_size(sum([file.size for file in files]))};{[file.filename for file in files]}")
    if not cloud.joinpath(user).exists():
        cloud.joinpath(user).mkdir()
    date = str(datetime.now().date())
    if not cloud.joinpath(user).joinpath(date).exists():
        cloud.joinpath(user).joinpath(date).mkdir()
    for file in files:
        with open(cloud.joinpath(user).joinpath(date).joinpath(file.filename), 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)
    return {"filename": [file.filename for file in files]}
