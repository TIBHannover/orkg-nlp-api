from typing import List
from pydantic import BaseModel

from app.models.common import Response, Annotation, Request


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

