# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends
from summarizer import Summarizer
from transformers import Pipeline

from app.common.util.decorators import log
from app.models.text import (
    ClassifySentenceRequest,
    ClassifySentenceResponse,
    SummarizeTextRequest,
    SummarizeTextResponse,
    ChatgptRequest,
    ChatgptResponse,
)
from app.services.text import ClassifierService, SummarizerService, ChatgptService

router = APIRouter(prefix="/text", tags=["text"])


@router.post("/summarize", response_model=SummarizeTextResponse, status_code=200)
@log(__name__)
def summarizes_text(
    request: SummarizeTextRequest,
    summarizer: Summarizer = Depends(SummarizerService.get_summarizer),
):
    service = SummarizerService(summarizer)
    return service.summarize(request.text, request.ratio)


@router.post("/classify", response_model=ClassifySentenceResponse, status_code=200)
@log(__name__)
def classifies_sentence(
    request: ClassifySentenceRequest,
    classifier: Pipeline = Depends(ClassifierService.get_classifier),
):
    service = ClassifierService(classifier)
    return service.classify(request.sentence, request.labels)


@router.post("/chatgpt", response_model=ChatgptResponse, status_code=200)
@log(__name__)
def chat_gpt(request: ChatgptRequest):
    chatgpt_service = ChatgptService()
    return chatgpt_service.completion(request.task_name, request.placeholders, request.temperature)
