from typing import List

from pydantic import BaseModel

from app.models.common import Request, Response, Template


class TemplatesRecommendationRequest(Request):
    title: str
    abstract: str
    top_n: int = 5


class TemplatesRecommendationResponse(Response):

    class Payload(BaseModel):
        templates: List[Template]

    payload: Payload
