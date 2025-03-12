import spacy
from domain.services import ExtractionService
from domain.entities import Entity, Relationship

class LocalExtractor(ExtractionService):
    def __init__(self):
        # Load the pre-trained spaCy model for English
        self.nlp = spacy.load("en_core_web_sm")
    
    def extract(self, text: str, entity_types: list = None, threshold: float = 0.5):
        doc = self.nlp(text)
        entities = []
        relationships = []  # Placeholder: Implement relationship extraction logic if needed
        
        for ent in doc.ents:
            # Filter by specified entity types if provided
            if not entity_types or ent.label_ in entity_types:
                entities.append(Entity(name=ent.text, type=ent.label_, confidence=1.0))
        return entities, relationships