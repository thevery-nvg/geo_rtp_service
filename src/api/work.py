import json
from fastapi import APIRouter, Request
from api.schemas import TransformRequest, BatchRequest
from api.services.convert_vba import conv_coordinates_full
from api.services.geo import raw_decode, geo_decode_gpx, google_decode, ready_data
from api.services.tomsk_autocad import autocad_decode_api

api_router = APIRouter(prefix="/api", tags=["Api"])


# --- Вспомогательные функции ---
async def _get_json_field(request: Request, field: str = "address") -> str:
    """Получить значение поля из JSON-запроса."""
    data = await request.json()
    return data.get(field, "")


def _make_decoder_endpoint(decode_func, with_gpx=False, screen=False):
    """Фабрика для создания эндпоинтов геокодеров."""
    async def endpoint(request: Request):
        address = await _get_json_field(request)
        decoded = decode_func(address, screen=screen) if screen else decode_func(address)
        return geo_decode_gpx(decoded) if with_gpx else decoded
    return endpoint


# --- Эндпоинты ---
api_router.post("/geocode_list")(_make_decoder_endpoint(raw_decode, screen=True))
api_router.post("/geocode_gpx")(_make_decoder_endpoint(raw_decode, with_gpx=True))
api_router.post("/google_list")(_make_decoder_endpoint(google_decode, screen=True))
api_router.post("/google_gpx")(_make_decoder_endpoint(google_decode, with_gpx=True))
api_router.post("/geocode_list_ready")(_make_decoder_endpoint(ready_data, screen=True))
api_router.post("/geocode_gpx_ready")(_make_decoder_endpoint(ready_data, with_gpx=True))


@api_router.post("/transform")
async def transform_value(request: TransformRequest):
    """Преобразовать одно значение координат."""
    return {
        "original": request.value,
        "transformed": conv_coordinates_full(request.value)
    }


@api_router.post("/transform_batch")
async def transform_batch(request: BatchRequest):
    """Преобразовать пакет координат."""
    return {
        "result": {key: conv_coordinates_full(value) for key, value in request.data.items()}
    }


@api_router.post("/draw_tomsk")
async def draw_tomsk(request: Request):
    """Обработка данных из AutoCAD (Tomsk)."""
    data = await request.json()
    print("Received JSON:", data)
    result = autocad_decode_api(data)
    return result  # можно вернуть json.dumps(result), если клиент ожидает строку
