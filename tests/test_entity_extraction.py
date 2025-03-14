"""
Module: test_entity_extraction
BDD-style tests for the file upload endpoint (/upload-file) using the ProjectPhoenixPlan.md file.
"""

import sys
import os
import pytest
import logging
from fastapi.testclient import TestClient

# Add the "src" directory to the Python path so that absolute imports work
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from api.main import app  # Import the FastAPI application using absolute imports

logger = logging.getLogger(__name__)
client = TestClient(app)

@pytest.fixture
def project_phoenix_plan_file():
    """
    Fixture to provide the path to the ProjectPhoenixPlan.md file for testing.
    
    Returns:
        str: The file path of ProjectPhoenixPlan.md.
    """
    file_path = os.path.join(os.path.dirname(__file__), "..", "docs", "ProjectPhoenixPlan.md")
    return file_path

def test_file_upload_extraction(project_phoenix_plan_file):
    """
    Test the /upload-file endpoint by uploading the ProjectPhoenixPlan.md file.
    
    Asserts:
      - The response status code is 200.
      - The JSON response contains an "entities" key with at least one entity.
      - The JSON response contains a "relationships" key.
    """
    with open(project_phoenix_plan_file, "rb") as f:
        files = {"file": ("ProjectPhoenixPlan.md", f, "text/markdown")}
        # Optionally, pass additional form fields for entity filtering and threshold
        data = {
            "entity_types": "PERSON,ORG",  # Comma-separated list (can be None if not needed)
            "relationship_threshold": 0.5
        }
        response = client.post("/upload-file", files=files, data=data)
    
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    json_response = response.json()
    
    # Assert that the response includes the 'entities' key and at least one entity is extracted.
    assert "entities" in json_response, "Response should include 'entities'"
    assert len(json_response["entities"]) > 0, "Expected at least one entity to be extracted"
    
    # Assert that the response includes the 'relationships' key.
    assert "relationships" in json_response, "Response should include 'relationships'"
    
    logger.info("Test successful: extracted %d entities and %d relationships.",
                len(json_response["entities"]), len(json_response["relationships"]))