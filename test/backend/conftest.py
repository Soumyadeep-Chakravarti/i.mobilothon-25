# test/backend/conftest.py
import pytest
from beanie import init_beanie
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient

from backend.app.src.core.config import settings
from backend.app.src.db.models import Project, User  # Import all models
from backend.app.src.main import app

# Use a separate test database name
TEST_MONGO_URI = settings.MONGO_URI.replace("v13_db", "v13_test_db")
TEST_DB_NAME = "v13_test_db"
TEST_DOCUMENT_MODELS = [User, Project]


@pytest.fixture(scope="session")
def anyio_backend():
    """Defines the asynchronous backend for pytest-asyncio."""
    return "asyncio"


@pytest.fixture(scope="session")
async def db_client():
    """Session-scoped fixture for the async MongoDB client."""
    client = AsyncIOMotorClient(TEST_MONGO_URI)
    await init_beanie(
        database=client[TEST_DB_NAME], document_models=TEST_DOCUMENT_MODELS
    )
    yield client
    # Clean up the test database after all tests are done
    client.drop_database(TEST_DB_NAME)


@pytest.fixture(scope="function", autouse=True)
async def cleanup_db(db_client):
    """Function-scoped fixture to clear all collections before each test."""
    yield
    # Delete all documents from all collections after test run
    for model in TEST_DOCUMENT_MODELS:
        await model.delete_all()


@pytest.fixture(scope="session")
async def client():
    """Test client fixture for making requests to the FastAPI app."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
