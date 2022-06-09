from typing import List

from fastapi import APIRouter

from app.models.text import SummarizeTextResponse, ClassifySentenceResponse, ClassifySentenceRequest
from app.services.text import TextService

router = APIRouter(
    prefix='/text',
    tags=['text']
)


@router.get('/summarize', response_model=SummarizeTextResponse, status_code=200)
def summarizes_text(text: str, ratio: float):
    text_service = TextService()
    return text_service.summarize(text, ratio)


@router.post('/classify', response_model=ClassifySentenceResponse, status_code=200)
def classifies_sentence(request: ClassifySentenceRequest):
    text_service = TextService()
    return text_service.classify(request.sentence, request.labels)
