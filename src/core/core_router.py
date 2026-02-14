from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


core_router = APIRouter(
    tags=["Core"],
)

core_router.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@core_router.get("/favicon.ico")
async def favicon():
    return RedirectResponse("https://img.icons8.com/3d-fluency/94/globe-africa.png")


@core_router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@core_router.get(path="/snake", response_class=HTMLResponse, )
async def snake(request: Request):
    return templates.TemplateResponse("snake.html", {"request": request})
