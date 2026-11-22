
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.database import Base, get_db
from src.main import app

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)

def test_create_task(client):
    response = client.post(
        "/tasks/",
        json={
            "title": "Organizar entregas",
            "description": "Separar encomendas",
            "priority": "alta",
            "status": "A Fazer"
        }
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Organizar entregas"

def test_list_tasks(client):
    client.post(
        "/tasks/",
        json={"title": "Conferir estoque"}
    )

    response = client.get("/tasks/")

    assert response.status_code == 200
    assert len(response.json()) == 1

def test_get_task(client):
    created = client.post(
        "/tasks/",
        json={"title": "Separar encomendas"}
    )

    task_id = created.json()["id"]

    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 200
    assert response.json()["title"] == "Separar encomendas"

def test_update_task(client):
    created = client.post(
        "/tasks/",
        json={"title": "Organizar estoque"}
    )

    task_id = created.json()["id"]

    response = client.put(
        f"/tasks/{task_id}",
        json={"status": "Concluído"}
    )

    assert response.status_code == 200
    assert response.json()["status"] == "Concluído"

def test_delete_task(client):
    created = client.post(
        "/tasks/",
        json={"title": "Conferir pedidos"}
    )

    task_id = created.json()["id"]

    response = client.delete(f"/tasks/{task_id}")

    assert response.status_code == 200

    check = client.get(f"/tasks/{task_id}")

    assert check.status_code == 404

def test_create_task_without_title(client):
    response = client.post(
        "/tasks/",
        json={
            "description": "Tarefa sem título"
        }
    )

    assert response.status_code == 422

def test_get_nonexistent_task(client):
    response = client.get("/tasks/999")

    assert response.status_code == 404


def test_filter_tasks_by_status(client):
    client.post(
        "/tasks/",
        json={"title": "Tarefa pendente", "status": "A Fazer"}
    )

    client.post(
        "/tasks/",
        json={"title": "Tarefa concluída", "status": "Concluído"}
    )

    response = client.get("/tasks/?status=A Fazer")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Tarefa pendente"


def test_filter_completed_tasks(client):
    client.post(
        "/tasks/",
        json={"title": "Tarefa pendente", "status": "A Fazer"}
    )

    client.post(
        "/tasks/",
        json={"title": "Tarefa concluída", "status": "Concluído"}
    )

    response = client.get("/tasks/?status=Concluído")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Tarefa concluída"


def test_list_all_tasks_without_filter(client):
    client.post(
        "/tasks/",
        json={"title": "Tarefa pendente", "status": "A Fazer"}
    )

    client.post(
        "/tasks/",
        json={"title": "Tarefa concluída", "status": "Concluído"}
    )

    response = client.get("/tasks/")

    assert response.status_code == 200
    assert len(response.json()) == 2

def test_home_page(client):
    response = client.get("/")

    assert response.status_code == 200
    assert "TaskFlow" in response.text
    assert "Nova tarefa" in response.text

def test_create_task_with_invalid_priority(client):
    response = client.post(
        "/tasks/",
        json={
            "title": "Tarefa com prioridade inválida",
            "priority": "urgente demais"
        }
    )

    assert response.status_code == 422