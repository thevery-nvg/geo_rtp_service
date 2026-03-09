import os
from fastapi import Request, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from pathlib import Path
import mimetypes
from datetime import datetime
from fastapi import APIRouter, UploadFile, File, Form, Request, Depends
import shutil
from typing import List
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse
from pathlib import Path
from core.config import settings

from loguru import logger
download_router = APIRouter(
    tags=["Download"])

download_router.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
cloud = Path(settings.cloud.url)
@download_router.get("/download", response_class=HTMLResponse)
async def download_page(request: Request):
    """Страница для скачивания файлов"""
    return templates.TemplateResponse("downloader.html", {"request": request})


@download_router.get("/api/files")
async def get_files(path: str = ""):
    """Получение списка файлов и папок"""
    try:
        base_path = cloud
        if path:
            current_path = base_path / path
        else:
            current_path = base_path

        if not current_path.exists():
            return JSONResponse(content={"error": "Path not found"}, status_code=404)

        items = []
        for item in current_path.iterdir():
            item_info = {
                "name": item.name,
                "path": str(item.relative_to(base_path)) if item != base_path else "",
                "is_dir": item.is_dir(),
                "size": item.stat().st_size if item.is_file() else 0,
                "modified": datetime.fromtimestamp(item.stat().st_mtime).isoformat()
            }
            items.append(item_info)

        # Сортируем: сначала папки, потом файлы
        items.sort(key=lambda x: (not x["is_dir"], x["name"].lower()))

        return {
            "current_path": path,
            "items": items,
            "parent_path": str(Path(path).parent) if path else None
        }
    except Exception as e:
        logger.error(f"Error getting files list: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)


@download_router.get("/api/download/{file_path:path}")
async def download_file(file_path: str):
    """Скачивание файла"""
    try:
        file_full_path = cloud / file_path

        if not file_full_path.exists():
            raise HTTPException(status_code=404, detail="File not found")

        if file_full_path.is_dir():
            raise HTTPException(status_code=400, detail="Cannot download directory")

        # Определяем MIME тип
        mime_type, _ = mimetypes.guess_type(str(file_full_path))
        if not mime_type:
            mime_type = "application/octet-stream"

        return FileResponse(
            path=file_full_path,
            filename=file_full_path.name,
            media_type=mime_type
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error downloading file: {e}")
        raise HTTPException(status_code=500, detail=str(e))