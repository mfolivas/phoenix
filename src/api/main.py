from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from domain.entities import Entity, Relationship
from infrastructure.local_extraction import LocalExtractor

app = FastAPI(title="Entity Extraction API")

# Request model for the API
class ExtractionRequest(BaseModel):
    content: str
    entity_types: Optional[List[str]] = None
    relationship_threshold: Optional[float] = 0.5

# Response model for the API
class ExtractionResponse(BaseModel):
    entities: List[Entity]
    relationships: List[Relationship]

# Instantiate our spaCy-based extraction service
extraction_service = LocalExtractor()

@app.post("/extract", response_model=ExtractionResponse)
async def extract_entities(request: ExtractionRequest):
    try:
        entities, relationships = extraction_service.extract(
            text=request.content,
            entity_types=request.entity_types,
            threshold=request.relationship_threshold
        )
        return ExtractionResponse(entities=entities, relationships=relationships)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))