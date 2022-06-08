from fastapi import APIRouter

from app.models.text import SummarizeTextResponse
from app.services.text import TextService

router = APIRouter(
    prefix='/text',
    tags=['text']
)


@router.get('/summarize', response_model=SummarizeTextResponse, status_code=200)
def summarizes_text(text: str, ratio: float):
    text_service = TextService()
    return text_service.summarize(text, ratio)
