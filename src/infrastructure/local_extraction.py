"""
Module: local_extraction
Provides a spaCy-based implementation of the ExtractionService for local Named Entity Recognition (NER)
and relationship identification using a simple heuristic.
"""

import spacy
import logging
from src.domain.services import ExtractionService
from src.domain.entities import Entity, Relationship
from src.config.config import SPACY_MODEL  # Import the spaCy model from the centralized config

# Get a logger for this module
logger = logging.getLogger(__name__)

class LocalExtractor(ExtractionService):
    """
    Implements the ExtractionService using spaCy for NER and a simple heuristic for relationship extraction.
    """
    def __init__(self):
        """
        Initializes the LocalExtractor by loading the spaCy model specified in the configuration.
        """
        try:
            # Load the spaCy model using the model name from config.py
            self.nlp = spacy.load(SPACY_MODEL)
            logger.info("spaCy model '%s' loaded successfully.", SPACY_MODEL)
        except Exception as e:
            logger.exception("Failed to load spaCy model '%s': %s", SPACY_MODEL, e)
            raise

    def extract(self, text: str, entity_types: list = None, threshold: float = 0.5):
        """
        Extracts entities from the input text and identifies relationships between entities in the same sentence.
        
        Args:
            text (str): The input text to be processed.
            entity_types (list, optional): List of specific entity types to filter.
            threshold (float, optional): Placeholder for future enhancements; not used in the current heuristic.
            
        Returns:
            Tuple[List[Entity], List[Relationship]]: A tuple containing the extracted entities and relationships.
        """
        logger.debug("Starting entity extraction with spaCy.")
        doc = self.nlp(text)
        spacy_entities = []  # To store raw spaCy entity spans for relationship extraction
        entities = []        # To store domain Entity objects
        
        # Extract entities using spaCy
        for ent in doc.ents:
            if not entity_types or ent.label_ in entity_types:
                spacy_entities.append(ent)
                entities.append(Entity(name=ent.text, type=ent.label_, confidence=1.0))
                logger.debug("Extracted entity: %s (%s)", ent.text, ent.label_)
        
        # Identify relationships between entities within the same sentence
        relationships = self.extract_relationships(doc, spacy_entities)
        logger.info("Extraction complete: %d entities and %d relationships identified.", len(entities), len(relationships))
        return entities, relationships

    def extract_relationships(self, doc, spacy_entities):
        """
        Identifies relationships between entities that appear in the same sentence.
        
        The heuristic is as follows:
          - For each sentence in the document, if two or more entities are present, create relationships between every pair.
          - The relationship 'strength' is calculated as the inverse of the token distance between the end of the first entity
            and the start of the second. A smaller distance implies a stronger relationship.
        
        Args:
            doc: The spaCy Doc object representing the processed text.
            spacy_entities: A list of spaCy Span objects representing extracted entities.
        
        Returns:
            List[Relationship]: A list of Relationship objects representing the identified relationships.
        """
        relationships = []
        
        # Process each sentence in the document
        for sent in doc.sents:
            # Filter entities that are within the boundaries of the sentence
            sent_entities = [ent for ent in spacy_entities if ent.start >= sent.start and ent.end <= sent.end]
            if len(sent_entities) >= 2:
                # Create a relationship for every pair of entities in the sentence
                for i in range(len(sent_entities)):
                    for j in range(i + 1, len(sent_entities)):
                        # Calculate token distance as a measure of proximity
                        distance = abs(sent_entities[j].start - sent_entities[i].end)
                        # Compute relationship strength (avoid division by zero)
                        strength = 1.0 / (distance if distance > 0 else 1)
                        relationships.append(Relationship(
                            source=sent_entities[i].text,
                            target=sent_entities[j].text,
                            relation="related_to",  # Default placeholder; can be refined further
                            strength=strength
                        ))
                        logger.debug("Created relationship: '%s' -> '%s' with strength %.3f",
                                     sent_entities[i].text, sent_entities[j].text, strength)
        return relationships