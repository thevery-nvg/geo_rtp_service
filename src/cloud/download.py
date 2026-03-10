from fastapi import HTTPException
from fastapi.responses import JSONResponse

import mimetypes
from fastapi import APIRouter, Request

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse
from pathlib import Path
from core.config import settings

from loguru import logger
from cloud.services import get_files_list, decode_file_path, find_file_case_insensitive

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
            current_path: Path = base_path / path
        else:
            current_path: Path = base_path

        if not current_path.exists():
            return JSONResponse(content={"error": "Path not found"}, status_code=404)
        items = get_files_list(current_path, base_path)

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
        # Декодируем путь к файлу
        decoded_path = decode_file_path(file_path)

        # Формируем полный путь к файлу
        file_full_path = cloud / decoded_path
        logger.info(f"Full file path: {file_full_path}")

        # Проверяем существование файла
        if not file_full_path.exists():
            # Пробуем найти файл без учета регистра
            found_path = find_file_case_insensitive(file_full_path)

            if found_path:
                file_full_path = found_path
            else:
                raise HTTPException(
                    status_code=404,
                    detail=f"File not found: {decoded_path}"
                )

        # Проверяем, что это не директория
        if file_full_path.is_dir():
            raise HTTPException(
                status_code=400,
                detail="Cannot download directory"
            )

        # Определяем MIME-тип
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
