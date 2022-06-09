from typing import List

from pydantic import BaseModel

from app.models.common import Predicate, Resource, Response, Request


class PredicatesClusteringRequest(Request):
    title: str
    abstract: str


class PredicatesClusteringResponse(Response):

    class Payload(BaseModel):
        predicates: List[Predicate]

    payload: Payload


class BioAssaysClusteringRequest(Request):
    text: str


class BioAssaysClusteringResponse(Response):

    class Payload(BaseModel):

        class BioAssayLabel(BaseModel):
            property: Predicate
            resources: List[Resource]

        labels: List[BioAssayLabel]

    payload: Payload
