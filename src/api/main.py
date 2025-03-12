"""
Module: main
Entry point for the FastAPI application providing the entity extraction endpoint.
"""

import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from src.domain.entities import Entity, Relationship
from src.infrastructure.local_extraction import LocalExtractor
from src.config.config import SPACY_MODEL

# Configure logging for the application
logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for more verbose output
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Entity Extraction API")

class ExtractionRequest(BaseModel):
    """
    Request model for the /extract endpoint.
    
    Attributes:
        content (str): The unstructured text or Markdown content.
        entity_types (Optional[List[str]]): Optional filter for specific entity types.
        relationship_threshold (Optional[float]): Threshold for relationship strength.
    """
    content: str
    entity_types: Optional[List[str]] = None
    relationship_threshold: Optional[float] = 0.5

class ExtractionResponse(BaseModel):
    """
    Response model for the /extract endpoint.
    
    Attributes:
        entities (List[Entity]): The list of extracted entities.
        relationships (List[Relationship]): The list of extracted relationships.
    """
    entities: List[Entity]
    relationships: List[Relationship]

# Instantiate our spaCy-based extraction service with config
extraction_service = LocalExtractor(config={"spacy_model": SPACY_MODEL})

@app.post("/extract", response_model=ExtractionResponse)
async def extract_entities(request: ExtractionRequest):
    """
    POST endpoint to extract entities from provided text content.
    
    Args:
        request (ExtractionRequest): The request payload with text content and optional filters.
        
    Returns:
        ExtractionResponse: A response containing extracted entities and relationships.
    """
    logger.info("Received extraction request.")
    try:
        entities, relationships = extraction_service.extract(
            text=request.content,
            entity_types=request.entity_types,
            threshold=request.relationship_threshold
        )
        logger.info("Extraction successful. Returning response.")
        return ExtractionResponse(entities=entities, relationships=relationships)
    except Exception as e:
        logger.error("Error during extraction: %s", e)
        raise HTTPException(status_code=500, detail=str(e))