# -*- coding: utf-8 -*-
from typing import Any, Dict, Optional, List

from pydantic import BaseModel

from app.models.common import Request, Response


class SummarizeTextRequest(Request):
    text: str
    ratio: float


class SummarizeTextResponse(Response):
    class Payload(BaseModel):
        summary: str

    payload: Payload


class ClassifySentenceRequest(Request):
    sentence: str
    labels: List[str]


class ClassifySentenceResponse(Response):
    class Payload(BaseModel):
        labels: List[str]
        scores: List[float]
        sequence: str

    payload: Payload


class ChatgptRequest(Request):
    task_name: str
    placeholders: Dict[str, Any]
    temperature: Optional[float]


class ChatgptResponse(Response):
    class Payload(BaseModel):
        arguments: Dict[str, Any]

    payload: Payload
