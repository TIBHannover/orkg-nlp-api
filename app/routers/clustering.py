from fastapi import APIRouter

from app.models.clustering import PredicatesClusteringResponse
from app.services.clustering import PredicatesService

router = APIRouter(
    prefix='/clustering',
    tags=['clustering']
)

predicates_service = PredicatesService()


@router.get('/predicates', response_model=PredicatesClusteringResponse, status_code=200)
def recommends_predicates(title: str, abstract: str):
    return predicates_service.recommend(title, abstract)

