from fastapi import APIRouter

from app.common.util.decorators import log
from app.models.annotation import CSNerAnnotationResponse, CSNerAnnotationRequest
from app.services.annotation import CSNerService

router = APIRouter(
    prefix='/annotation',
    tags=['annotation']
)


@router.post('/csner', response_model=CSNerAnnotationResponse, status_code=200)
@log(__name__)
def annotates_paper(request: CSNerAnnotationRequest):
    cs_ner_service = CSNerService()
    return cs_ner_service.annotate(request.title, request.abstract)
