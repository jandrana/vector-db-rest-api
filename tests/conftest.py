import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

os.environ.setdefault("COHERE_API_KEY", "test")

import pytest

from fastapi.testclient import TestClient

from app.main import app
from app.api.deps import get_db
from app.db.database import Database
from app.db.inverted_index import InvertedIndex
from app.services import index_service
from app.services import search_service


class DummyPersistence:
    def __init__(self):
        self.actions = []

    def save_action(self, action, data):
        self.actions.append((action, data))

    def load_actions(self):
        return []


@pytest.fixture
def test_db(tmp_path):
    """Fresh Database instance for testing without persistence."""
    db = Database()
    db.persistence = DummyPersistence()
    db.libraries = {}
    db.documents = {}
    db.chunks = {}
    db.inverted_index = InvertedIndex()
    db.lib_num = db.doc_num = db.chunk_num = 0
    db.is_loading = False

    if not hasattr(db, "_save_action"):
        db._save_action = db.persistence.save_action

    return db


@pytest.fixture(autouse=True)
def stub_embeddings(monkeypatch):
    """Globally stub embed generation to avoid external Cohere API calls during tests."""

    def fake_generate(texts, input_type="search_document"):
        return [[1.0, 0.0] for _ in texts]

    monkeypatch.setattr(index_service, "generate_embeddings", fake_generate)
    monkeypatch.setattr(search_service, "generate_embeddings", fake_generate)
    yield


@pytest.fixture
def client(test_db, monkeypatch):

    app.dependency_overrides[get_db] = lambda: test_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.pop(get_db, None)
