from typing import List, Any

from pydantic import BaseModel

from app.models.common import Response, Request


class SummarizeTextResponse(Response):

    class Payload(BaseModel):
        summary: str

    payload: Payload


class ClassifySentenceResponse(Response):

    class Payload(BaseModel):
        labels: List[str]
        scores: List[float]
        sequence: str

    payload: Payload


class ClassifySentenceRequest(Request):
    sentence: str
    labels: List[str]
