import pytest
import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))
from app import app as flask_app


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        yield client


def test_index_returns_200(client):
    response = client.get("/")
    assert response.status_code == 200


def test_index_contains_app_name(client):
    response = client.get("/")
    data = json.loads(response.data)
    assert data["app"] == "DevOps Demo App"


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "ok"


def test_get_all_tasks(client):
    response = client.get("/tasks")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_task_by_id(client):
    response = client.get("/tasks/1")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["id"] == 1


def test_get_task_not_found(client):
    response = client.get("/tasks/9999")
    assert response.status_code == 404


def test_create_task(client):
    payload = {"title": "Nueva tarea de prueba"}
    response = client.post(
        "/tasks",
        data=json.dumps(payload),
        content_type="application/json"
    )
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["title"] == "Nueva tarea de prueba"
    assert data["done"] is False


def test_create_task_missing_title(client):
    response = client.post(
        "/tasks",
        data=json.dumps({}),
        content_type="application/json"
    )
    assert response.status_code == 400


def test_update_task(client):
    payload = {"done": True}
    response = client.put(
        "/tasks/1",
        data=json.dumps(payload),
        content_type="application/json"
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["done"] is True


def test_delete_task(client):
    # Primero creamos una tarea para borrarla
    payload = {"title": "Tarea a eliminar"}
    create_resp = client.post(
        "/tasks",
        data=json.dumps(payload),
        content_type="application/json"
    )
    task_id = json.loads(create_resp.data)["id"]

    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200

    # Verificar que ya no existe
    get_resp = client.get(f"/tasks/{task_id}")
    assert get_resp.status_code == 404
