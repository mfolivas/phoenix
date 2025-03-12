"""
Module: entities
Defines the core domain models for the application, including Entity and Relationship.
"""

from pydantic import BaseModel

class Entity(BaseModel):
    """
    Represents a named entity extracted from text.
    
    Attributes:
        name (str): The text of the entity.
        type (str): The category/type of the entity (e.g., PERSON, ORG).
        confidence (float): A confidence score for the extracted entity.
    """
    name: str
    type: str
    confidence: float

class Relationship(BaseModel):
    """
    Represents a relationship between two entities.
    
    Attributes:
        source (str): The source entity.
        target (str): The target entity.
        relation (str): The type of relationship between entities.
        strength (float): A measure of the relationship's strength.
    """
    source: str
    target: str
    relation: str
    strength: float