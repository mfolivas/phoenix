"""
Module: test_entity_extraction
BDD-style tests for the entity extraction endpoint using the ProjectPhoenixPlan.md file as input.
"""

import os
import pytest
from fastapi.testclient import TestClient
from src.api.main import app
import logging

# Get a logger for the test module
logger = logging.getLogger(__name__)

client = TestClient(app)

@pytest.fixture
def project_phoenix_plan_text():
    """
    Fixture to load the content from ProjectPhoenixPlan.md for testing.
    
    Returns:
        str: The content of the ProjectPhoenixPlan.md file.
    """
    file_path = os.path.join(os.path.dirname(__file__), "..", "docs", "ProjectPhoenixPlan.md")
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    logger.info("Loaded ProjectPhoenixPlan.md for testing.")
    return content

def test_entity_extraction(project_phoenix_plan_text):
    """
    Given the content of ProjectPhoenixPlan.md,
    When the content is submitted to the /extract endpoint,
    Then the response should include a list of extracted entities.
    """
    payload = {
        "content": project_phoenix_plan_text,
        "entity_types": None,
        "relationship_threshold": 0.5
    }
    response = client.post("/extract", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert "entities" in data
    assert len(data["entities"]) > 0
    logger.info("Test successful: %d entities extracted.", len(data["entities"]))