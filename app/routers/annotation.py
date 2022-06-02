from fastapi import APIRouter

from app.models.annotation import CSNerAnnotationResponse
from app.services.annotation import CSNerService

router = APIRouter(
    prefix='/annotation',
    tags=['annotation']
)


@router.get('/csner', response_model=CSNerAnnotationResponse, status_code=200)
def annotates_paper(title: str = None, abstract: str = None):
    cs_ner_service = CSNerService()
    return cs_ner_service.annotate(title, abstract)
