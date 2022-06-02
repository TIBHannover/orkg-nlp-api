import datetime

from uuid import UUID
from pydantic import BaseModel
from typing import List


class Response(BaseModel):
    timestamp: datetime.datetime
    uuid: UUID


class Predicate(BaseModel):
    id: str
    label: str


class Resource(BaseModel):
    id: str
    label: str


class Annotation(BaseModel):
    concept: str
    entities: List[str]
