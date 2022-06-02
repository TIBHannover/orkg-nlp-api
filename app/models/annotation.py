from typing import List
from pydantic import BaseModel

from app.models.common import Response, Annotation


class PaperAnnotations(BaseModel):
    title: List[Annotation]
    abstract: List[Annotation]


class CSNerAnnotationResponse(Response):
    annotations: PaperAnnotations
