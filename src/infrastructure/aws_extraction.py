import boto3
from domain.services import ExtractionService
from domain.entities import Entity, Relationship

class AWSComprehendExtractor(ExtractionService):
    def __init__(self, region_name="us-east-1"):
        self.comprehend = boto3.client("comprehend", region_name=region_name)

    def extract(self, text: str, entity_types: list = None, threshold: float = 0.5):
        response = self.comprehend.detect_entities(Text=text, LanguageCode="en")
        entities = []
        relationships = []  # Implement relationship extraction if needed
        
        for ent in response.get("Entities", []):
            if not entity_types or ent["Type"] in entity_types:
                entities.append(Entity(name=ent["Text"], type=ent["Type"], confidence=ent["Score"]))
        return entities, relationships