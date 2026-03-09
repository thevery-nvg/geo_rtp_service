
from fastapi import  HTTPException
from fastapi.responses import  JSONResponse

import base64
from urllib.parse import unquote
import mimetypes
from datetime import datetime
from fastapi import APIRouter, Request

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


        # Пробуем декодировать как base64 если путь начинается с b64_
        if file_path.startswith('b64_'):
            try:
                # Убираем префикс и декодируем base64
                encoded_path = file_path[4:]  # убираем 'b64_'
                decoded_bytes = base64.b64decode(encoded_path)
                decoded_path = decoded_bytes.decode('utf-8')
                logger.info(f"Decoded base64 path: {decoded_path}")
            except:
                # Если не получилось, используем как есть
                decoded_path = unquote(file_path)
        else:
            decoded_path = unquote(file_path)

        # Очищаем путь от возможных проблемных символов
        decoded_path = decoded_path.replace('\x00', '')  # убираем нулевые байты

        file_full_path = cloud / decoded_path
        logger.info(f"Full file path: {file_full_path}")

        if not file_full_path.exists():
            # Пробуем найти файл без учета регистра
            found = False
            if file_full_path.parent.exists():
                for f in file_full_path.parent.iterdir():
                    if f.name.lower() == file_full_path.name.lower():
                        file_full_path = f
                        found = True
                        break

            if not found:
                raise HTTPException(status_code=404, detail=f"File not found: {decoded_path}")

        if file_full_path.is_dir():
            raise HTTPException(status_code=400, detail="Cannot download directory")

        # Читаем файл и отдаем как есть
        mime_type, _ = mimetypes.guess_type(str(file_full_path))
        if not mime_type:
            mime_type = "application/octet-stream"

        # Отдаем файл с правильными заголовками
        return FileResponse(
            path=file_full_path,
            filename=file_full_path.name,
            media_type=mime_type,
            headers={
                "Content-Disposition": f"attachment; filename=\"{file_full_path.name}\"",
                "Content-Transfer-Encoding": "binary",
                "Accept-Ranges": "bytes",
                "Cache-Control": "no-cache"
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error downloading file: {e}")
        raise HTTPException(status_code=500, detail=str(e))