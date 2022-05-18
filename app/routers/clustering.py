from fastapi import APIRouter

from app.models.clustering import PredicatesClusteringResponse, BioAssaysClusteringResponse
from app.services.clustering import PredicatesService, BioassaysService

router = APIRouter(
    prefix='/clustering',
    tags=['clustering']
)


@router.get('/predicates', response_model=PredicatesClusteringResponse, status_code=200)
def recommends_predicates(title: str, abstract: str):
    predicates_service = PredicatesService()
    return predicates_service.recommend(title, abstract)


@router.get('/bioassays', response_model=BioAssaysClusteringResponse, status_code=200)
def semantifies_bioassays(text: str):
    bioassays_service = BioassaysService()
    return bioassays_service.semantify(text)
