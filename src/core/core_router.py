from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Optional

from auth import current_user
from auth.models import User

core_router = APIRouter(
    tags=["Core"],
)

core_router.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
favicon_path = "src\\img\\favicon.png"


# @core_router.get('/favicon.ico', include_in_schema=False)
# async def favicon():
#     return FileResponse(favicon_path)


@core_router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@core_router.get(path="/snake", response_class=HTMLResponse,)
async def snake(request: Request,user: User = Depends(current_user)):
    return templates.TemplateResponse("snake.html", {"request": request,"user":user})
