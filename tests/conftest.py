import os
import sys
import tempfile
import pytest
from fastapi.testclient import TestClient

os.environ.setdefault("COHERE_API_KEY", "test")

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app.main import get_application
from app.core.container import DIContainer
from app.core.config import Settings


@pytest.fixture
def test_db_file(tmp_path):
    """Create a temporary database file for testing."""
    temp_file = tempfile.NamedTemporaryFile(
        mode="w", delete=False, suffix=".jsonl", dir=tmp_path
    )
    temp_file.close()
    yield temp_file.name
    try:
        os.unlink(temp_file.name)
    except:
        pass


@pytest.fixture
def test_container(test_db_file, monkeypatch):
    """Create a test container with isolated dependencies."""
    monkeypatch.setenv("DB_FILE", test_db_file)
    settings = Settings(
        DB_FILE=test_db_file,
        COHERE_API_KEY="test",
        EMBEDDING_MODEL="test-model",
        _env_file=None,
    )
    container = DIContainer(settings=settings)
    yield container


@pytest.fixture
def test_db(test_container):
    """Backward compatibility fixture - returns the test container."""
    return test_container


@pytest.fixture(autouse=True)
def stub_embeddings(monkeypatch):
    """Globally stub embed generation to avoid external Cohere API calls during tests."""

    def patched_method(self, texts, *args, **kwargs):
        """Mock embedding generation that accepts any arguments."""
        return [[1.0, 0.0] for _ in texts]

    from app.services.embedding.embedding_provider import CohereEmbeddingProvider

    monkeypatch.setattr(CohereEmbeddingProvider, "generate_embeddings", patched_method)
    yield


@pytest.fixture
def client(test_container):
    """Create a test client with dependency injection."""
    app = get_application()
    app.state.container = test_container

    with TestClient(app) as c:
        yield c

    app.state.container = None
