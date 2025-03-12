"""
Module: services
Defines an abstract interface for entity extraction.
"""

from abc import ABC, abstractmethod
from typing import List, Tuple
from domain.entities import Entity, Relationship

class ExtractionService(ABC):
    """
    Abstract base class that defines the interface for an entity extraction service.
    Implementations must provide the extract method.
    """
    @abstractmethod
    def extract(self, text: str, entity_types: list = None, threshold: float = 0.5) -> Tuple[List[Entity], List[Relationship]]:
        """
        Extracts entities and relationships from the given text.
        
        Args:
            text (str): The input text for extraction.
            entity_types (list, optional): List of entity types to filter. Defaults to None.
            threshold (float, optional): The minimum threshold for relationship strength. Defaults to 0.5.
        
        Returns:
            Tuple[List[Entity], List[Relationship]]: A tuple containing a list of entities and a list of relationships.
        """
        pass