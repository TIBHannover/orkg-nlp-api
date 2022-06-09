import json
from typing import Dict, List

from pydantic import conlist

from app.models.common import Response, Request


class ExtractTableRequest(Request):
    page_number: int
    region: conlist(float, min_items=4, max_items=4)
    lattice: bool = False

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class ExtractTableResponse(Response):
    table: Dict[str, List[str]]
