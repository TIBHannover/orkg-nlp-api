from typing import List

from app.models.common import Predicate, Response


class PredicatesClusteringResponse(Response):
    predicates: List[Predicate]

