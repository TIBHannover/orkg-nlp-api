import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel


class Response(BaseModel):
    timestamp: datetime.datetime
    uuid: UUID


class Request(BaseModel):
    pass


class Predicate(BaseModel):
    id: str
    label: str


class Resource(BaseModel):
    id: str
    label: str


class Annotation(BaseModel):
    concept: str
    entities: List[str]
