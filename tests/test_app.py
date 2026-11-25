import pytest
from app import app


@pytest.fixture()
def client():
    app.config.update(TESTING=True)
    with app.test_client() as test_client:
        yield test_client


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "/health" in response.get_json()["endpoints"]


def test_hello_default(client):
    assert client.get("/hello").get_json()["message"] == "Hello, Developer!"


def test_hello_custom_name(client):
    assert client.get("/hello?name=Swaroopa").get_json()["message"] == "Hello, Swaroopa!"


def test_hello_blank_name(client):
    assert client.get("/hello?name=%20%20").get_json()["message"] == "Hello, Developer!"
