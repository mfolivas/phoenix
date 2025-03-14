"""
Module: test_entity_extraction
BDD-style tests for the entity extraction endpoint using the ProjectPhoenixPlan.md file as input.
"""

import os
import random
import pytest
from fastapi.testclient import TestClient
from src.api.main import app
import logging

# Get a logger for the test module
logger = logging.getLogger(__name__)

client = TestClient(app)

import spacy
from spacy.util import minibatch
from spacy.training import Example


def test_spacy_trainging_model():
    training_data = [
        ("What is the price of 10 bananas?", {"entities": [(21, 23, "QUANTITY"), (24, 31, "PRODUCT")]}),
        ("I need to buy 5 apples from the store", {"entities": [(13, 14, "QUANTITY"), (15, 21, "PRODUCT")]}),
        ("How much would 3 laptops cost?", {"entities": [(15, 16, "QUANTITY"), (17, 24, "PRODUCT")]}),
        ("Add 2 bottles of water to my cart", {"entities": [(4, 5, "QUANTITY"), (6, 23, "PRODUCT")]}),
        ("We require 20 chairs for the meeting", {"entities": [(11, 13, "QUANTITY"), (14, 20, "PRODUCT")]}),
        ("Can you order 12 pencils for the office?", {"entities": [(14, 16, "QUANTITY"), (17, 24, "PRODUCT")]}),
        ("The recipe calls for 500 grams of flour", {"entities": [(20, 23, "QUANTITY"), (33, 38, "PRODUCT")]}),
        ("I would like to purchase 6 notebooks", {"entities": [(25, 26, "QUANTITY"), (27, 36, "PRODUCT")]}),
        ("They delivered 100 bricks yesterday", {"entities": [(15, 18, "QUANTITY"), (19, 25, "PRODUCT")]}),
        ("Please add 4 t-shirts to my order", {"entities": [(11, 12, "QUANTITY"), (13, 21, "PRODUCT")]}),
        ("What's the total for 8 coffee mugs?", {"entities": [(20, 21, "QUANTITY"), (22, 33, "PRODUCT")]}),
        ("Find me prices for 15 headphones", {"entities": [(18, 20, "QUANTITY"), (21, 31, "PRODUCT")]}),
        ("Do you sell packages of 24 paper towels?", {"entities": [(22, 24, "QUANTITY"), (25, 37, "PRODUCT")]}),
        ("I need a quote for 50 desk lamps", {"entities": [(19, 21, "QUANTITY"), (22, 32, "PRODUCT")]}),
        ("Can I get a discount on 7 keyboards?", {"entities": [(24, 25, "QUANTITY"), (26, 35, "PRODUCT")]}),
        ("How much are 30 meters of cable?", {"entities": [(13, 15, "QUANTITY"), (25, 30, "PRODUCT")]}),
        ("Add 1 smartphone to my wishlist", {"entities": [(4, 5, "QUANTITY"), (6, 16, "PRODUCT")]}),
        ("We're looking to order 25 monitors", {"entities": [(22, 24, "QUANTITY"), (25, 33, "PRODUCT")]}),
        ("The package contains 60 screws", {"entities": [(20, 22, "QUANTITY"), (23, 29, "PRODUCT")]}),
        ("I'm interested in buying 3 printers", {"entities": [(25, 26, "QUANTITY"), (27, 35, "PRODUCT")]}),
    ]

    nlp = spacy.load("en_core_web_md")
    if 'ner' not in nlp.pipe_names:
        ner = nlp.create_pipe("ner")
        nlp.add_pipe("ner")
    else:
        ner = nlp.get_pipe("ner")
        
    
    
    for _, annotations in training_data:
        for ent in annotations.get("entities"):
            if ent[2] not in ner.labels:
                ner.add_label(ent[2])
                
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
    with nlp.select_pipes(disable=other_pipes):
        optimizer = nlp.initialize()
        
        epochs = 50
        for epoch in range(epochs):
            random.shuffle(training_data)
            losses = {}
            batches = minibatch(training_data, size=2)
            for batch in batches:
                examples = []
                for text, annotations in batch:
                    doc = nlp.make_doc(text)
                    example = Example.from_dict(doc, annotations)
                    examples.append(example)
                nlp.update(examples, sgd=optimizer, drop=0.5, losses=losses)
                
            logger.info(f"Epoch {epoch} - Losses: {losses}")
            
    nlp.to_disk('custom_ner_model')
    
    training_nlp = spacy.load('custom_ner_model')
    test_text = [
        "How much for 3 oranges?",
        "I want 15 chairs for the conference",
        "Can you give me the price for 6 desks?"
    ]
    
    for text in test_text:
        doc = training_nlp(text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        
        # Assert that entities were found
        assert len(entities) > 0, f"No entities found in: {text}"
        
        # Assert specific entity detection for each test text
        if text == "How much for 3 oranges?":
            assert ("3", "QUANTITY") in entities, "Failed to identify '3' as QUANTITY"
            assert ("oranges", "PRODUCT") in entities, "Failed to identify 'oranges' as PRODUCT"
        elif text == "I want 15 chairs for the conference":
            assert ("15", "QUANTITY") in entities, "Failed to identify '15' as QUANTITY" 
            assert ("chairs", "PRODUCT") in entities, "Failed to identify 'chairs' as PRODUCT"
        elif text == "Can you give me the price for 6 desks?":
            assert ("6", "QUANTITY") in entities, "Failed to identify '6' as QUANTITY"
            assert ("desks", "PRODUCT") in entities, "Failed to identify 'desks' as PRODUCT"
        
        # Assert that all identified entities have the expected labels
        for ent_text, ent_label in entities:
            assert ent_label in ["QUANTITY", "PRODUCT"], f"Unexpected entity label: {ent_label}"




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
    # Ensure that at least one entity is extracted
    assert len(data["entities"]) > 0
    logger.info("Test successful: %d entities extracted.", len(data["entities"]))

def test_entity_extraction_with_specific_markdown():
    """
    Given a specific markdown snippet about Project Phoenix,
    When the content is submitted to the /extract endpoint,
    Then the response should include correctly structured entities and relationships.
    """
    markdown_content = """## Product Roadmap

Project Phoenix will introduce three main product lines over the next 18 months, focusing on end-to-end solutions that incorporate Redwood Tech Solutions' proprietary machine learning libraries"""

    payload = {
        "content": markdown_content,
        "entity_types": None,  # Extract all entity types
        "relationship_threshold": 0.5
    }
    
    response = client.post("/extract", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    
    # Verify response structure
    assert "entities" in data
    assert "relationships" in data
    
    # Verify entities were extracted
    assert len(data["entities"]) > 0
    
    # Inspect structure of entities
    for entity in data["entities"]:
        assert "id" in entity
        assert "type" in entity
        assert "text" in entity
        assert "start_idx" in entity
        assert "end_idx" in entity
    
    # Inspect structure of relationships if any exist
    if data["relationships"]:
        for relationship in data["relationships"]:
            assert "source_id" in relationship
            assert "target_id" in relationship
            assert "type" in relationship
            assert "confidence" in relationship
            # Verify relationship confidence meets threshold
            assert relationship["confidence"] >= 0.5
    
    logger.info("Test successful: %d entities and %d relationships extracted.", 
                len(data["entities"]), len(data["relationships"]))