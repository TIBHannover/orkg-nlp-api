from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class Response(BaseModel):
    timestamp: datetime
    uuid: UUID


class Request(BaseModel):
    pass


class Predicate(BaseModel):
    id: str
    label: str


class Template(BaseModel):
    id: str
    label: str


class Resource(BaseModel):
    id: str
    label: str


class Annotation(BaseModel):
    concept: str
    entities: List[str]


class BaseORMObject(BaseModel):

    id: Optional[UUID]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
