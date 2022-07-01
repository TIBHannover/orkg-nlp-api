from typing import Any, Dict, List
from uuid import UUID

from pydantic import BaseModel

from app import AppConfig
from app.models.common import Request, Response, BaseORMObject


class BaseFeedback(BaseModel):
    request: Dict[str, Any]
    response: Dict[str, Any]


class FeedbackCreateRequest(Request):

    class Feedback(BaseFeedback):
        service_name: AppConfig.get_service_names_as_enum()

    feedback: Feedback


class FeedbackCreateResponse(Response):

    class Payload(BaseModel):
        id: UUID

    payload: Payload


class FeedbackReadAllResponse(Response):

    class Payload(BaseModel):

        class Feedback(BaseFeedback, BaseORMObject):
            # In case one enum value has been excluded and still exists in the DB, we still want to retrieve it.
            service_name: str

        feedbacks: List[Feedback]

    payload: Payload
