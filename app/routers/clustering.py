from fastapi import APIRouter, Depends
from orkgnlp.clustering import BioassaysSemantifier, PredicatesRecommender

from app.common.util.decorators import log
from app.models.clustering import PredicatesClusteringResponse, BioAssaysClusteringResponse, \
    PredicatesClusteringRequest, BioAssaysClusteringRequest
from app.services.clustering import PredicatesService, BioassaysService

router = APIRouter(
    prefix='/clustering',
    tags=['clustering']
)


@router.post('/predicates', response_model=PredicatesClusteringResponse, status_code=200)
@log(__name__)
def recommends_predicates(
        request: PredicatesClusteringRequest,
        recommender: PredicatesRecommender = Depends(PredicatesService.get_recommender)
):
    service = PredicatesService(recommender)
    return service.recommend(request.title, request.abstract)


@router.post('/bioassays', response_model=BioAssaysClusteringResponse, status_code=200)
@log(__name__)
def semantifies_bioassays(
        request: BioAssaysClusteringRequest,
        semantifier: BioassaysSemantifier = Depends(BioassaysService.get_semantifier)
):
    service = BioassaysService(semantifier)
    return service.semantify(request.text)
