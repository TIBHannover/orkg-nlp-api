# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.common.util.decorators import log
from app.db.connection import get_db
from app.models.feedback import (
    FeedbackCreateRequest,
    FeedbackCreateResponse,
    FeedbackReadAllResponse,
)
from app.services.feedback import FeedbackService

router = APIRouter(prefix="/feedback", tags=["feedback"])


@router.post("/", response_model=FeedbackCreateResponse, status_code=200)
@log(__name__)
def creates_feedback(request: FeedbackCreateRequest, db: Session = Depends(get_db)):
    feedback_service = FeedbackService(db)
    return feedback_service.create(
        request.feedback.service_name, request.feedback.request, request.feedback.response
    )


@router.get("/", response_model=FeedbackReadAllResponse, status_code=200)
@log(__name__)
def reads_all_feedbacks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    feedback_service = FeedbackService(db)
    return feedback_service.read_all(skip=skip, limit=limit)
