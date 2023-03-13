# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends
from orkgnlp.annotation import AgriNer, CSNer

from app.common.util.decorators import log
from app.models.annotation import (
    AgriNerAnnotationRequest,
    AgriNerAnnotationResponse,
    CSNerAnnotationRequest,
    CSNerAnnotationResponse,
)
from app.services.annotation import AgriNerService, CSNerService

router = APIRouter(prefix="/annotation", tags=["annotation"])


@router.post("/csner", response_model=CSNerAnnotationResponse, status_code=200)
@log(__name__)
def annotates_cs_paper(
    request: CSNerAnnotationRequest, annotator: CSNer = Depends(CSNerService.get_annotator)
):
    service = CSNerService(annotator)
    return service.annotate(request.title, request.abstract)


@router.post("/agriner", response_model=AgriNerAnnotationResponse, status_code=200)
@log(__name__)
def annotates_agri_paper(
    request: AgriNerAnnotationRequest, annotator: AgriNer = Depends(AgriNerService.get_annotator)
):
    service = AgriNerService(annotator)
    return service.annotate(request.title)
