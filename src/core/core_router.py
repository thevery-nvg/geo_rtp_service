from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

core_router = APIRouter(
    tags=["Core"],
)

core_router.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@core_router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@core_router.get("/snake", response_class=HTMLResponse)
async def snake(request: Request):
    return templates.TemplateResponse("snake.html", {"request": request})
