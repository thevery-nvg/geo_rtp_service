from pathlib import Path
from datetime import datetime
import base64
from typing import Optional
from urllib.parse import unquote

from core.config import settings
from loguru import logger

cloud = Path(settings.cloud.url)


def format_size(size_in_bytes):
    units = ['Б', 'КБ', 'МБ', 'ГБ', 'ТБ']
    unit_index = 0
    while size_in_bytes >= 1024 and unit_index < len(units) - 1:
        size_in_bytes /= 1024
        unit_index += 1
    return f"{size_in_bytes:.2f} {units[unit_index]}"


def get_files_list(current_path: Path, base_path: Path):
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
    return items


def decode_file_path(file_path: str) -> str:
    """Декодирует путь к файлу из base64 или URL-кодировки"""
    try:
        # Пробуем декодировать как base64 если путь начинается с b64_
        if file_path.startswith('b64_'):
            try:
                # Убираем префикс и декодируем base64
                encoded_path = file_path[4:]  # убираем 'b64_'
                decoded_bytes = base64.b64decode(encoded_path)
                decoded_path = decoded_bytes.decode('utf-8')
                logger.info(f"Decoded base64 path: {decoded_path}")
            except Exception as e:
                # Если не получилось, используем как есть с URL-декодированием
                logger.warning(f"Failed to decode base64 path: {e}, falling back to URL decode")
                decoded_path = unquote(file_path)
        else:
            decoded_path = unquote(file_path)

        # Очищаем путь от возможных проблемных символов
        decoded_path = decoded_path.replace('\x00', '')  # убираем нулевые байты

        return decoded_path
    except Exception as e:
        logger.error(f"Error decoding file path: {e}")
        # В случае любой ошибки возвращаем исходный путь с URL-декодированием
        return unquote(file_path).replace('\x00', '')


def find_file_case_insensitive(file_path: Path) -> Optional[Path]:
    """Пытается найти файл без учета регистра"""
    try:
        if not file_path.parent.exists():
            return None

        for f in file_path.parent.iterdir():
            if f.name.lower() == file_path.name.lower():
                return f
    except Exception as e:
        logger.error(f"Error during case-insensitive file search: {e}")

    return None
