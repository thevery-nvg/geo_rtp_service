import logging
import sys
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from loguru import logger
from sqladmin import Admin

from api import api_router
from auth import auth_router, users_router
from auth.admin import UserAdmin, authentication_backend
from auth.users_proxy import fastapi_users_proxy_router
from cloud.uploader import upload_router
from core.config import settings
from core.core_router import core_router
from core.models import db_helper
from google_sheets.sheets_main import gs_router


@asynccontextmanager
async def lifespan(application: FastAPI):
    # startup

    # shutdown
    yield
    await db_helper.dispose()


app = FastAPI(
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

app.include_router(auth_router, prefix=settings.prefix.api)
app.include_router(users_router, prefix=settings.prefix.api)
app.include_router(fastapi_users_proxy_router)
app.include_router(api_router)
app.include_router(core_router)
app.include_router(upload_router)
app.include_router(gs_router)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# admin--------------
admin = Admin(
    app=app,
    authentication_backend=authentication_backend,
    session_maker=db_helper.session_factory,
)
admin.add_view(UserAdmin)
# admin--------------


@app.middleware("http")
async def log_requests(request: Request, call_next):
    try:
        response = await call_next(request)
    except Exception as e:
        logger.warning(f"Invalid HTTP request received: {e}")
        raise

    return response


@app.exception_handler(404)
async def custom_404_handler(request: Request, _):
    return templates.TemplateResponse("404.html", {"request": request})


@app.exception_handler(401)
async def custom_401_handler(request: Request, _):
    return RedirectResponse("/login_proxy")


# Перехват логов uvicorn.access
uvicorn_access_logger = logging.getLogger("uvicorn.access")
uvicorn_access_logger.handlers = []


# Кастомный обработчик для перенаправления логов в loguru
class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Преобразуем запись лога в строку
        message = self.format(record)
        logger.log(level, message)


# Добавляем кастомный обработчик
uvicorn_access_logger.addHandler(InterceptHandler())

if __name__ == "__main__":
    logger.remove()  # Удаляем стандартный обработчик
    logger.add(sys.stdout, format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")
    logger.add("logs/main.txt", rotation="10 MB")
    uvicorn.run("main:app", host=settings.run.host, port=settings.run.port)
