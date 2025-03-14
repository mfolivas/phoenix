"""
Module: main
Entry point for the FastAPI application that provides an upload-file endpoint for entity extraction.
This endpoint accepts a file upload along with optional form fields to filter entity types and set a relationship threshold.
"""

import logging
from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Depends
from pydantic import BaseModel
from typing import List, Optional
from src.domain.entities import Entity, Relationship
from src.config.config import EXTRACTION_MODE  # e.g., "local" or "aws", and SPACY_MODEL is defined here
from src.infrastructure.local_extraction import LocalExtractor
from src.infrastructure.aws_extraction import AWSComprehendExtractor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Entity Extraction API")

class ExtractionResponse(BaseModel):
    """
    Response model for the /upload-file endpoint.
    
    Attributes:
        entities (List[Entity]): List of extracted entities.
        relationships (List[Relationship]): List of extracted relationships.
    """
    entities: List[Entity]
    relationships: List[Relationship]

def get_extraction_service():
    """
    Dependency injection function to select the appropriate extraction service.
    
    Returns:
        AWSComprehendExtractor if EXTRACTION_MODE == "aws",
        otherwise returns LocalExtractor (spaCy-based).
    
    Execution:
        - For local development, set EXTRACTION_MODE to "local" in config/config.py.
        - For AWS extraction, set EXTRACTION_MODE to "aws" and configure AWS credentials.
    """
    if EXTRACTION_MODE == "aws":
        logger.info("Using AWS Comprehend extractor.")
        return AWSComprehendExtractor()
    else:
        logger.info("Using local spaCy extractor.")
        return LocalExtractor()

@app.post("/upload-file", response_model=ExtractionResponse)
async def upload_file(
    file: UploadFile = File(...),
    entity_types: Optional[str] = Form(None),  # Comma-separated list of entity types (e.g., "PERSON,ORG")
    relationship_threshold: Optional[float] = Form(0.5),
    extraction_service = Depends(get_extraction_service)
):
    """
    Endpoint to upload a file and extract entities and relationships.
    
    The file should contain plain text or Markdown content.
    Optionally, a comma-separated list of entity types can be provided to filter the extraction.
    
    Args:
        file (UploadFile): The file to be processed.
        entity_types (Optional[str]): Comma-separated entity types to filter (e.g., "PERSON,ORG").
        relationship_threshold (Optional[float]): Threshold for filtering weak relationships.
        extraction_service: The extraction service injected via dependency injection.
    
    Returns:
        ExtractionResponse: A JSON object containing lists of extracted entities and relationships.
    """
    try:
        # Read the uploaded file content and decode to text
        contents = await file.read()
        text = contents.decode('utf-8')
        
        # Process the entity_types form field into a list if provided
        types_list = [t.strip() for t in entity_types.split(",")] if entity_types else None
        
        # Extract entities and relationships using the selected extraction service
        entities, relationships = extraction_service.extract(
            text=text,
            entity_types=types_list,
            threshold=relationship_threshold
        )
        
        # Convert each Entity and Relationship model to a dictionary using model_dump (Pydantic v2)
        entities_dict = [entity.model_dump() for entity in entities]
        relationships_dict = [rel.model_dump() for rel in relationships]
        
        return ExtractionResponse(entities=entities_dict, relationships=relationships_dict)
    except Exception as e:
        logger.error("Error processing file upload: %s", e)
        raise HTTPException(status_code=500, detail=str(e))