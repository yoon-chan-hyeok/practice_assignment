import shutil
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.repositories import json_knowledge as repo

@pytest.fixture
def isolated(tmp_path, monkeypatch):
    path = tmp_path / "knowledge.json"
    shutil.copy2(Path(__file__).resolve().parents[1]/"data/knowledge.seed.json", path)
    monkeypatch.setattr(repo, "DATA", path)
    with TestClient(app) as client:
        yield client, path
