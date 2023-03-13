# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends
from orkgnlp.nli import TemplatesRecommender

from app.common.util.decorators import log
from app.models.nli import (
    TemplatesRecommendationRequest,
    TemplatesRecommendationResponse,
)
from app.services.nli import TemplatesService

router = APIRouter(prefix="/nli", tags=["nli"])


@router.post("/templates", response_model=TemplatesRecommendationResponse, status_code=200)
@log(__name__)
def recommends_templates(
    request: TemplatesRecommendationRequest,
    recommender: TemplatesRecommender = Depends(TemplatesService.get_recommender),
):
    service = TemplatesService(recommender)
    return service.recommend(request.title, request.abstract, request.top_n)
