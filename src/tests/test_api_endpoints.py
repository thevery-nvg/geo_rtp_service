import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_geocode_list_returns_coordinates(monkeypatch):
    monkeypatch.setattr("api.services.geo_utils.raw_decode", lambda data, screen=False: [(60.1, 70.2)])
    response = client.post("/api/geocode_list", json={"address": ["some input"]})
    assert response.status_code == 200
    assert response.json() == [(60.1, 70.2)]


def test_geocode_gpx_returns_xml(monkeypatch):
    monkeypatch.setattr("api.services.raw_decode", lambda data: [(60.1, 70.2)])
    monkeypatch.setattr("api.services.geo_decode_gpx", lambda x: "<gpx>test</gpx>")
    response = client.post("/api/geocode_gpx", json={"address": ["some input"]})
    assert response.status_code == 200
    assert "<gpx>" in response.text


def test_google_list_and_gpx(monkeypatch):
    monkeypatch.setattr("api.services.google_decode", lambda data, screen=False: [(60.1, 70.2)])
    monkeypatch.setattr("api.services.geo_decode_gpx", lambda x: "<gpx>data</gpx>")

    resp1 = client.post("/api/google_list", json={"address": ["test"]})
    resp2 = client.post("/api/google_gpx", json={"address": ["test"]})
    assert resp1.status_code == 200
    assert resp2.status_code == 200


def test_transform_single(monkeypatch):
    monkeypatch.setattr("api.services.convert_vba.conv_coordinates_full", lambda x: "ok")
    resp = client.post("/api/transform", json={"value": "test"})
    assert resp.status_code == 200
    assert resp.json() == {"original": "test", "transformed": "ok"}


def test_transform_batch(monkeypatch):
    monkeypatch.setattr("api.services.convert_vba.conv_coordinates_full", lambda x: f"tr_{x}")
    data = {"data": {"a": "v1", "b": "v2"}}
    resp = client.post("/api/transform_batch", json=data)
    assert resp.status_code == 200
    assert resp.json()["result"] == {"a": "tr_v1", "b": "tr_v2"}


def test_draw_tomsk_returns_json(monkeypatch):
    monkeypatch.setattr("api.services.tomsk_autocad.autocad_decode_api", lambda data: {"ok": True})
    resp = client.post("/api/draw_tomsk", json={"x": 1})
    assert resp.status_code == 200
    assert resp.json() == {"ok": True}


def test_ready_data_endpoints(monkeypatch):
    monkeypatch.setattr("api.services.geo_utils.ready_data", lambda data, screen=False: [(1.0, 2.0)])
    monkeypatch.setattr("api.services.geo_utils.geo_decode_gpx", lambda x: "<gpx></gpx>")
    r1 = client.post("/api/geocode_list_ready", json={"address": ["test"]})
    r2 = client.post("/api/geocode_gpx_ready", json={"address": ["test"]})
    assert r1.status_code == 200
    assert r2.status_code == 200
