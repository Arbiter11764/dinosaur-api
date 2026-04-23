from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app # Your FastAPI File

client = TestClient(app)

def test_get_dinosaur_success():
    mock_response = MagicMock()
    mock_response.data = [{"id" : 1, "name": "Tyrannosaurus Rex"}]

    with 
