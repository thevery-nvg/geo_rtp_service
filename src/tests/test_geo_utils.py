import re
import pytest
from api.services.geo import (
    _clean_data, _zfillr, convert_coordinates_full, raw_decode,
    google_decode, ready_data, geo_decode_gpx, convert_to_dms_format,
    decimal_degrees_to_str
)


def test_clean_data_removes_invalid_chars():
    assert _clean_data("N60°12.345E70°45.678") == "N6012.345E7045.678"


def test_zfillr_padding_and_trimming():
    assert _zfillr("123", 8) == "12300000"
    assert _zfillr("123456789", 8) == "12345678"


def test_convert_coordinates_full_simple_pattern():
    pattern = r"N?(\d{2}\.\d+)E?(\d{2}\.\d+)"
    coord = "N60.123E70.456"
    lat, lon = convert_coordinates_full(pattern, coord)
    assert (round(lat, 3), round(lon, 3)) == (60.123, 70.456)


def test_convert_to_dms_format_returns_expected_format():
    res = convert_to_dms_format("N62.90617° E74.41833°")
    assert "N62" in res and "E74" in res


def test_decimal_degrees_to_str_format():
    res = decimal_degrees_to_str(60.1234, 70.9876)
    assert res.startswith("N") and "E" in res and "°" in res


def test_raw_decode_recognizes_pattern():
    data = ["N6000123.45E07000123.45"]
    result = raw_decode(data)
    assert isinstance(result, list)
    assert all(isinstance(x, tuple) for x in result)


def test_google_decode_parses_pairs_correctly():
    data = "60.12345,70.67890 60.98765,70.54321"
    coords = google_decode(data)
    assert len(coords) == 2
    assert all(isinstance(x, tuple) for x in coords)


def test_ready_data_parses_lines():
    text = "60.123 70.456\n61.000 71.000"
    result = ready_data(text)
    assert len(result) == 2
    assert result[0] == (60.123, 70.456)


def test_geo_decode_gpx_generates_valid_xml():
    coords = [(60.123, 70.456)]
    xml = geo_decode_gpx(coords)
    assert xml.strip().startswith('<?xml')
    assert re.search(r'<wpt lat="60\.123" lon="70\.456">', xml)
