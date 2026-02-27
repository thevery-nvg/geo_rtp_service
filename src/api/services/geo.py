import re
import random
from functools import reduce
from typing import List, Tuple, Union
from pyproj import Proj

# --- Constants ---
WGS84 = Proj('epsg:4326')

COORD_PATTERNS = {
    "pa": (r"N(0?\d{2})(\d{2})(\d{2}\.\d{1,3})", r"E(0?\d{2})(\d{2})(\d{2}\.\d{1,3})"),
    "pb": (r"N(0?\d{2})(\d{1,2}\.\d{1,3})", r"E(0?\d{2})(\d{1,2}\.\d{1,3})"),
    "pc": (r"N(\d{2}\.\d+)", r"E(\d{2}\.\d+)"),
    "pd": (r"(\d{2}\.\d+)", r"(\d{2}\.\d+)")
}


# --- Utility functions ---
def _clean_data(data: str) -> str:
    """Очищает строку от лишних символов, заменяя запятые на точки."""
    x=re.sub(r"[^NE0-9.]", "", data.replace(",", "."))
    y=re.sub(r"\d{2}\.\d{2}\.\d{4}","",x)
    return y


def _zfillr(value: Union[str, float], width: int = 8) -> str:
    """Обрезает или дополняет число нулями справа до указанной длины."""
    s = str(value)
    return s[:width] if len(s) > width else s.ljust(width, "0")


def _to_dms(value: float) -> Tuple[int, int, int]:
    """Перевод десятичной координаты в градусы, минуты, секунды."""
    deg = int(value)
    minutes = int((value - deg) * 60)
    seconds = int((value - deg - minutes / 60) * 3600)
    return deg, minutes, seconds


def decimal_degrees_to_str(lat: float, lon: float) -> str:
    """Форматирует координаты в виде Nxx.xxxx° Exx.xxxx°."""
    deg_symbol = "° "
    return f"N{_zfillr(lat)}{deg_symbol}E{_zfillr(lon)}{deg_symbol}"


def convert_to_dms_format(coord_str: str) -> str:
    """Преобразует строку формата 'N62.90617° E74.41833°' в 'N62 54.37\tE74 25.10'."""
    try:
        lat_str, lon_str = coord_str.split()
        lat = float(lat_str[1:-1])
        lon = float(lon_str[1:-1])
    except (ValueError, IndexError):
        return ""

    def _to_deg_min(val: float) -> str:
        deg = int(val)
        minutes = (val - deg) * 60
        return f"{deg} {minutes:.2f}"

    return f"N{_to_deg_min(lat)}\tE{_to_deg_min(lon)}"



def convert_to_dms_format2(coord_str: str) -> str:
    """Преобразует строку формата 'N62.90617° E74.41833°' в 'N62 54.37\tE74 25.10'."""
    try:
        lat_str, lon_str = coord_str.split()
        lat = float(lat_str[1:-1])
        lon = float(lon_str[1:-1])
    except (ValueError, IndexError):
        return ""

    def _to_deg_min(val: float) -> str:
        deg = int(val)
        minutes = (val - deg) * 60
        sec=(minutes-int(minutes))*60
        minutes = int(minutes)
        return f"{deg} {minutes} {sec:.2f}"

    return f"N{_to_deg_min(lat)}\tE{_to_deg_min(lon)}"

# --- Coordinate parsing ---
def convert_coordinates_full(pattern: str, coord_str: str) -> Tuple[float, float]:
    """Преобразует координату по регулярному шаблону в (lat, lon)."""
    match = re.fullmatch(pattern, _clean_data(coord_str))
    if not match:
        return 0.0, 0.0

    parts = match.groups()
    if len(parts) == 2:
        lat, lon = map(float, parts)
    elif len(parts) == 4:
        lat = float(parts[0]) + float(parts[1]) / 60
        lon = float(parts[2]) + float(parts[3]) / 60
    elif len(parts) == 6:
        lat = float(parts[0]) + float(parts[1]) / 60 + float(parts[2]) / 3600
        lon = float(parts[3]) + float(parts[4]) / 60 + float(parts[5]) / 3600
    else:
        return 0.0, 0.0

    return round(lat, 5), round(lon, 5)


def raw_decode(data: List[str], fi,fo, screen: bool = False) -> List[Union[Tuple[float, float], str]]:
    """Декодирует строковые координаты в список (lat, lon) или в текст для экрана."""

    if not data:
        return []
    if "pa" in fi:
        pattern = COORD_PATTERNS["pa"]
    elif "pb" in fi:
        pattern = COORD_PATTERNS["pb"]
    elif "pc" in fi:
        pattern = COORD_PATTERNS["pc"]
    else:
        pattern = COORD_PATTERNS["pd"]
    combined = _clean_data(reduce(lambda x, y: x + y, data))

    p_lat=pattern[0]
    p_lon = pattern[1]
    full_pattern = f"{p_lat}{p_lon}"
    lat_matches = re.findall(p_lat, combined)
    lon_matches = re.findall(p_lon, combined)
    coords = []
    formatted = []

    for lat, lon in zip(lat_matches, lon_matches):
        coord_str = "N" + "".join(lat) + "E" + "".join(lon)
        coord = convert_coordinates_full(full_pattern, coord_str)
        coords.append(coord)
        formatted.append(decimal_degrees_to_str(*coord))

    if "pa" in fo:
        res = [convert_to_dms_format2(x) for x in formatted] if screen else coords
    elif "pb" in fo:
        res = [convert_to_dms_format(x) for x in formatted] if screen else coords
    elif "pc" in fo:
        res = formatted if screen else coords
    else:
        res = coords
    return res


def google_decode(data: str, screen: bool = False) -> List[Union[Tuple[float, float], str]]:
    """Парсит координаты из строк Google Maps."""
    p=re.compile(r'<coordinates>\n.+\n.+</coordinates>')
    c=re.search(p,data)
    matches = re.findall(r"\d{2}\.\d+", c.group(0))
    if not matches:
        return []

    lats, lons = matches[::2], matches[1::2]
    lats, lons =lons,lats
    coords = list(zip(map(float, lats), map(float, lons)))
    formatted = [decimal_degrees_to_str(lat, lon) for lat, lon in coords]

    return [convert_to_dms_format(x) for x in formatted] if screen else coords


def ready_data(data: str, screen: bool = False) -> List[Union[Tuple[float, float], str]]:
    """Парсит данные вида '56.12345 74.98765' построчно."""
    lines = [line.strip() for line in data.splitlines() if line.strip()]
    pattern = re.compile(r"\d{2}[\.,]\d{3,5}")
    coords, formatted = [], []

    for line in lines:
        matches = [m.replace(",", ".") for m in re.findall(pattern, line)]
        if len(matches) < 2:
            continue
        lat, lon = map(float, matches[:2])
        coords.append((lat, lon))
        formatted.append(decimal_degrees_to_str(lat, lon))

    return formatted if screen else coords


# --- GPX output ---
def geo_decode_gpx(coords: List[Tuple[float, float]]) -> str:
    """Генерирует GPX XML из списка координат."""
    header = """<?xml version="1.0" encoding="UTF-8"?>
<gpx xmlns="http://www.topografix.com/GPX/1/1"
     creator="MapSource 6.16.3"
     version="1.1"
     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
     xsi:schemaLocation="http://www.topografix.com/GPX/1/1 
     http://www.topografix.com/GPX/1/1/gpx.xsd">
  <metadata>
    <link href="http://www.garmin.com"><text>Garmin International</text></link>
    <time>2024-01-23T12:24:21Z</time>
  </metadata>
"""
    body = ""
    base_height = random.randint(40, 60)

    for idx, (lat, lon) in enumerate(coords, start=1):
        height = base_height + random.randint(1, 5)
        body += f'''  <wpt lat="{lat}" lon="{lon}">
    <ele>{height}</ele>
    <time>2024-01-16T12:56:09Z</time>
    <name>{idx:03}</name>
    <sym>Flag, Green</sym>
  </wpt>\n'''

    return header + body + "</gpx>\n"
