from pyproj import CRS, Transformer
import re
from typing import Tuple


def parse_utm_input(utm_string: str) -> Tuple[int, int, int, bool]:
    """
    Разбирает строку UTM формата '43 V 381324 6751887'.

    Возвращает:
        (zone, easting, northing, northern_hemisphere)
    """
    parts = utm_string.strip().split()
    if len(parts) < 4:
        raise ValueError(f"Некорректный формат UTM: '{utm_string}' (ожидается 4 части)")

    zone = int(parts[0])
    lat_band = parts[1].upper()
    easting = int(parts[2])
    northing = int(parts[3])
    northern_hemisphere = lat_band >= "N"

    return zone, easting, northing, northern_hemisphere


def utm_to_latlon(utm_string: str) -> str:
    """
    Конвертирует координаты из формата UTM в широту/долготу (DMS).

    Пример:
        '43 V 381324 6751887' → 'N61 02 15.0 E76 59 20.5'
    """
    # Если в строке уже есть N/E, значит, это не UTM.
    if re.search(r"[nNsSeE]\d+", utm_string):
        return utm_string

    try:
        zone, easting, northing, northern = parse_utm_input(utm_string)
    except Exception:
        return utm_string  # возвращаем как есть, если формат не UTM

    crs_utm = CRS.from_proj4(
        f"+proj=utm +zone={zone} +datum=WGS84 +units=m +no_defs{' +south' if not northern else ''}"
    )
    crs_wgs84 = CRS.from_epsg(4326)
    transformer = Transformer.from_crs(crs_utm, crs_wgs84, always_xy=True)

    lon, lat = transformer.transform(easting, northing)
    return degrees_to_dms(lat, lon)


def degrees_to_dms(lat: float, lon: float) -> str:
    """
    Переводит десятичные градусы в строку формата:
        'N61 02 15.0 E76 59 20.5'
    """
    def to_dms(deg: float) -> Tuple[int, int, float]:
        d = int(deg)
        m_float = abs(deg - d) * 60
        m = int(m_float)
        s = round((m_float - m) * 60, 1)
        return d, m, s

    lat_d, lat_m, lat_s = to_dms(lat)
    lon_d, lon_m, lon_s = to_dms(lon)

    lat_dir = "N" if lat >= 0 else "S"
    lon_dir = "E" if lon >= 0 else "W"

    return f"{lat_dir}{abs(lat_d)} {lat_m:02} {lat_s:04.1f} {lon_dir}{abs(lon_d)} {lon_m:02} {lon_s:04.1f}"


def convert_coordinates(coord_str: str) -> str:
    """
    Добавляет символы ° ´ ´´ для вывода координат в человекочитаемом виде.
    Если строка уже содержит символ '°', возвращает как есть.
    """
    if "°" in coord_str:
        return coord_str

    parts = coord_str.split()
    if len(parts) < 6:
        return coord_str  # если формат неожиданный, не ломаем

    deg_symbol = "° "
    min_symbol = "´"
    sec_symbol = "´´"

    lat = f"{parts[0]}{parts[1]}{deg_symbol}{parts[2]}{min_symbol}{parts[3]}{sec_symbol}"
    lon = f"{parts[4]}{parts[5]}{deg_symbol}{parts[6]}{min_symbol}{parts[7]}{sec_symbol}"

    return f"{lat} {lon}"


def conv_coordinates_full(utm_string: str) -> str:
    """
    Конечная функция для конвертации строки UTM → формат координат (с символами ° ´ ´´).

    Пример:
        '43 V 381324 6751887' → 'N61° 02´15.0´´ E76° 59´20.5´´'
    """
    latlon_str = utm_to_latlon(utm_string)
    formatted = convert_coordinates(latlon_str)
    return formatted
