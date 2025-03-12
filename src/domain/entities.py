from pydantic import BaseModel

class Entity(BaseModel):
    name: str
    type: str
    confidence: float

class Relationship(BaseModel):
    source: str
    target: str
    relation: str
    strength: float