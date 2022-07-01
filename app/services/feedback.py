from typing import Any, Dict

from sqlalchemy.orm import Session

from app.common.errors import OrkgNlpApiError
from app.common.services.wrapper import ResponseWrapper
from app.db import crud
from app.db.models.feedback import Feedback
from app.services import OrkgNlpApiService


class FeedbackService(OrkgNlpApiService):

    def __init__(self, db: Session):
        self.db = db

    def create(self, service_name: str, request: Dict[str, Any], response: Dict[str, Any]):

        if not request or not response:
            raise OrkgNlpApiError('"request" and "response" must be valued JSON objects.', self.__class__)

        feedback = Feedback(service_name=service_name, request=request, response=response)

        crud.create(self.db, feedback)

        return ResponseWrapper.wrap_json({'id': feedback.id})

    def read_all(self, skip: int = 0, limit: int = 100):
        feedbacks = crud.query_all(self.db, Feedback, skip, limit)
        return ResponseWrapper.wrap_json({'feedbacks': feedbacks})
