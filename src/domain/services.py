from abc import ABC, abstractmethod
from typing import List, Tuple
from domain.entities import Entity, Relationship

class ExtractionService(ABC):
    @abstractmethod
    def extract(self, text: str, entity_types: list = None, threshold: float = 0.5) -> Tuple[List[Entity], List[Relationship]]:
        pass