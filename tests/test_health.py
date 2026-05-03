from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    """El servidor debe responder ok"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["estado"] == "ok"

def test_crear_item():
    """Debe crear un item y devolver id"""
    response = client.post("/items/", json={
        "nombre": "Item de prueba",
        "descripcion": "Descripcion de prueba",
        "activo": True
    })
    assert response.status_code == 201
    data = response.json()
    assert data["nombre"] == "Item de prueba"
    assert data["id"] == 1

def test_obtener_items():
    """Debe retornar lista de items"""
    response = client.get("/items/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_obtener_item_no_existe():
    """Debe retornar 404 si no existe"""
    response = client.get("/items/999")
    assert response.status_code == 404