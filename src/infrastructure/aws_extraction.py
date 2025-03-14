"""
Module: aws_extraction
Provides an AWS Comprehend-based implementation of the ExtractionService.
"""

import boto3
import logging
from src.domain.services import ExtractionService
from src.domain.entities import Entity, Relationship

# Get a logger for this module
logger = logging.getLogger(__name__)

class AWSComprehendExtractor(ExtractionService):
    """
    Implements the ExtractionService using AWS Comprehend for entity extraction.
    """
    def __init__(self, region_name="us-east-1"):
        """
        Initializes the AWSComprehendExtractor with the specified AWS region.
        
        Args:
            region_name (str): AWS region to use for Comprehend. Defaults to "us-east-1".
        """
        try:
            self.comprehend = boto3.client("comprehend", region_name=region_name)
            logger.info("AWS Comprehend client initialized for region %s.", region_name)
        except Exception as e:
            logger.exception("Failed to initialize AWS Comprehend client: %s", e)
            raise

    def extract(self, text: str, entity_types: list = None, threshold: float = 0.5):
        """
        Extracts entities from the input text using AWS Comprehend.
        
        Args:
            text (str): The input text to process.
            entity_types (list, optional): Specific entity types to filter. Defaults to None.
            threshold (float, optional): Relationship strength threshold (not used in this implementation).
        
        Returns:
            Tuple[List[Entity], List[Relationship]]: Extracted entities and (placeholder) relationships.
        """
        logger.debug("Starting entity extraction using AWS Comprehend.")
        response = self.comprehend.detect_entities(Text=text, LanguageCode="en")
        entities = []
        relationships = []  # Placeholder for relationship extraction logic
        
        for ent in response.get("Entities", []):
            if not entity_types or ent["Type"] in entity_types:
                entities.append(Entity(name=ent["Text"], type=ent["Type"], confidence=ent["Score"]))
                logger.debug("Extracted AWS entity: %s (%s)", ent["Text"], ent["Type"])
                
        logger.info("AWS extraction complete. %d entities extracted.", len(entities))
        return entities, relationships