from fastapi.testclient import TestClient
import pytest

from .main import app
from .deps import get_db
from .database import Base, create_engine, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="function", autouse=True)
def clear_tables():
    yield
    meta = Base.metadata  # type: ignore
    session = TestingSessionLocal()

    for table in reversed(meta.sorted_tables):
        session.execute(table.delete())
    session.commit()


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


client = TestClient(app)


def create_customer(name, description):
    return client.post("/api/customer", json={"name": name, "description": description})


def test_create_customer():
    response = create_customer("Company name", "Company description")
    assert response.status_code == 201

    data = response.json()
    assert "id" in data
    assert data["name"] == "Company name"
    assert data["description"] == "Company description"


def test_get_customer():
    company_data = {"name": "Company", "description": "description"}
    data = create_customer(**company_data).json()
    response = client.get(f"/api/customer/{data['id']}")
    assert response.status_code == 200
    assert data == response.json()


def test_get_customers():
    company_data = {"name": "Company", "description": "description"}
    create_customer(**company_data)
    create_customer(**company_data)

    response = client.get("/api/customer")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_csv_customers():
    company_data = {"name": "Company", "description": "description"}
    data = create_customer(**company_data).json()
    data2 = create_customer(**company_data).json()

    response = client.get("/api/customer/export")

    assert data['id'] in str(response.content)
    assert data2['id'] in str(response.content)
