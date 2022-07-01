from fastapi import APIRouter

from app.common.util.decorators import log
from app.models.text import SummarizeTextResponse, ClassifySentenceResponse, ClassifySentenceRequest, \
    SummarizeTextRequest
from app.services.text import SummarizerService, ClassifierService

router = APIRouter(
    prefix='/text',
    tags=['text']
)


@router.post('/summarize', response_model=SummarizeTextResponse, status_code=200)
@log(__name__)
def summarizes_text(request: SummarizeTextRequest):
    text_service = SummarizerService()
    return text_service.summarize(request.text, request.ratio)


@router.post('/classify', response_model=ClassifySentenceResponse, status_code=200)
@log(__name__)
def classifies_sentence(request: ClassifySentenceRequest):
    text_service = ClassifierService()
    return text_service.classify(request.sentence, request.labels)
