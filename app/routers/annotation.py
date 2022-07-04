from fastapi import APIRouter, Depends
from orkgnlp.annotation import CSNer

from app.common.util.decorators import log
from app.models.annotation import CSNerAnnotationResponse, CSNerAnnotationRequest
from app.services.annotation import CSNerService

router = APIRouter(
    prefix='/annotation',
    tags=['annotation']
)


@router.post('/csner', response_model=CSNerAnnotationResponse, status_code=200)
@log(__name__)
def annotates_paper(
        request: CSNerAnnotationRequest,
        annotator: CSNer = Depends(CSNerService.get_annotator)
):
    service = CSNerService(annotator)
    return service.annotate(request.title, request.abstract)
