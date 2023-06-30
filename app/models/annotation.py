# -*- coding: utf-8 -*-
from typing import List

from pydantic import BaseModel

from app.models.common import Annotation, Request, Response


class ResearchFieldClassifierRequest(Request):
    raw_input: str = None
    top_n: int = None


class ResearchFieldClassifierResponse(Response):
    class Payload(BaseModel):
        class ResearchFieldClassification(BaseModel):
            research_field: str
            score: float

        annotations: List[ResearchFieldClassification]

    payload: Payload


class CSNerAnnotationRequest(Request):
    title: str = None
    abstract: str = None


class CSNerAnnotationResponse(Response):
    class Payload(BaseModel):
        class TitleAbstractAnnotations(BaseModel):
            title: List[Annotation]
            abstract: List[Annotation]

        annotations: TitleAbstractAnnotations

    payload: Payload


class AgriNerAnnotationRequest(Request):
    title: str


class AgriNerAnnotationResponse(Response):
    class Payload(BaseModel):
        annotations: List[Annotation]

    payload: Payload
