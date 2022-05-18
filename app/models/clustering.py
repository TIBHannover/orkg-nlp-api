from typing import List

from pydantic import BaseModel

from app.models.common import Predicate, Resource, Response


class PredicatesClusteringResponse(Response):
    predicates: List[Predicate]


class BioAssayLabel(BaseModel):
    property: Predicate
    resources: List[Resource]


class BioAssaysClusteringResponse(Response):
    labels: List[BioAssayLabel]
