from fastapi import APIRouter

from app.models.clustering import PredicatesClusteringResponse, BioAssaysClusteringResponse, \
    PredicatesClusteringRequest, BioAssaysClusteringRequest
from app.services.clustering import PredicatesService, BioassaysService

router = APIRouter(
    prefix='/clustering',
    tags=['clustering']
)


@router.post('/predicates', response_model=PredicatesClusteringResponse, status_code=200)
def recommends_predicates(request: PredicatesClusteringRequest):
    predicates_service = PredicatesService()
    return predicates_service.recommend(request.title, request.abstract)


@router.post('/bioassays', response_model=BioAssaysClusteringResponse, status_code=200)
def semantifies_bioassays(request: BioAssaysClusteringRequest):
    bioassays_service = BioassaysService()
    return bioassays_service.semantify(request.text)
