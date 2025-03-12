"""
Module: local_extraction
Provides a spaCy-based implementation of the ExtractionService for local NER.
"""

import spacy
import logging
from domain.services import ExtractionService
from domain.entities import Entity, Relationship

# Get a logger for this module
logger = logging.getLogger(__name__)

class LocalExtractor(ExtractionService):
    """
    Implements the ExtractionService using spaCy for Named Entity Recognition.
    """
    def __init__(self):
        """
        Initializes the LocalExtractor and loads the spaCy model.
        """
        try:
            self.nlp = spacy.load("en_core_web_sm")
            logger.info("spaCy model 'en_core_web_sm' loaded successfully.")
        except Exception as e:
            logger.exception("Failed to load spaCy model: %s", e)
            raise

    def extract(self, text: str, entity_types: list = None, threshold: float = 0.5):
        """
        Extracts entities from the input text using spaCy.
        
        Args:
            text (str): The input text to process.
            entity_types (list, optional): Specific entity types to filter. Defaults to None.
            threshold (float, optional): Relationship strength threshold (not used in this implementation).
        
        Returns:
            Tuple[List[Entity], List[Relationship]]: Extracted entities and (placeholder) relationships.
        """
        logger.debug("Starting entity extraction with spaCy.")
        doc = self.nlp(text)
        entities = []
        relationships = []  # Placeholder for relationship extraction logic

        for ent in doc.ents:
            if not entity_types or ent.label_ in entity_types:
                entities.append(Entity(name=ent.text, type=ent.label_, confidence=1.0))
                logger.debug("Extracted entity: %s (%s)", ent.text, ent.label_)
                
        logger.info("Extraction complete. %d entities extracted.", len(entities))
        return entities, relationships