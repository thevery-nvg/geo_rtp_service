from fastapi import APIRouter, UploadFile, File, Form, Request, Depends
import shutil
from typing import List

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse
from pathlib import Path
from auth import current_user_strict
from auth.models import User

upload_router = APIRouter(
    tags=["Upload"])

upload_router.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
cloud=Path.cwd().joinpath("cloud")


@upload_router.get("/upload", response_class=HTMLResponse)
async def upload_page(request: Request,user: User = Depends(current_user_strict)):
    return templates.TemplateResponse("upload.html", {"request": request})


@upload_router.post("/upload")
async def upload_images(files: List[UploadFile] = File(...)):
    for file in files:
        with open(cloud.joinpath(file.filename), 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)
    return {"filename": [file.filename for file in files]}
