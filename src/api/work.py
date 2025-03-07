from fastapi import Request, APIRouter
from .schemas import TransformRequest
from api.services.convert_vba import conv_coordinates_full
from api.services.geo import raw_decode, geo_decode_gpx, google_decode, ready_data
import json
from api.services.tomsk_autocad import autocad_decode_api

api_router = APIRouter(
    prefix="/api",
    tags=["Api"],
)


@api_router.post("/geocode_list")
async def geocode_list(request: Request):
    """Получаем данные из input на странице,возвращается список преобразованных координат в окно
    output """
    d = await request.json()
    x = raw_decode(d["address"], screen=True)
    return x


@api_router.post("/geocode_gpx")
async def geocode_gpx(request: Request):
    """Скачивание"""
    d = await request.json()
    x = raw_decode(d["address"])
    return geo_decode_gpx(x)


@api_router.post("/google_list")
async def google_list(request: Request):
    d = await request.json()
    x = google_decode(d["address"], screen=True)
    return x


@api_router.post("/google_gpx")
async def google_gpx(request: Request):
    """Скачивание"""
    d = await request.json()
    x = google_decode(d["address"])
    return geo_decode_gpx(x)


@api_router.post("/transform")
async def transform_value(request: TransformRequest):
    transformed_value = conv_coordinates_full(request.value)
    return {"original": request.value, "transformed": transformed_value}


@api_router.post("/draw_tomsk")
async def try_parse_vba_json(request: Request):
    data = await request.json()
    print("Received JSON:", data)
    a = autocad_decode_api(data)
    output = json.dumps(a)
    # возможно стоит возвращать  output,потом будет видно работает или нет.
    # Но вроде работало
    return a


@api_router.post("/geocode_list_ready")
async def geocode_list_ready(request: Request):
    d = await request.json()
    x = ready_data(d["address"], screen=True)
    return x


@api_router.post("/geocode_gpx_ready")
async def geocode_gpx_ready(request: Request):
    d = await request.json()
    x = ready_data(d["address"])
    return geo_decode_gpx(x)
