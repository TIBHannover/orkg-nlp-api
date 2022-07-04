from fastapi.testclient import TestClient

from app.main import app
from app.services.clustering import BioassaysService, PredicatesService
from app.tests.mock.mock_clustering import BioAssaysSemantifierMock, PredicatesRecommenderMock

app.dependency_overrides[BioassaysService.get_semantifier] = BioAssaysSemantifierMock.get_semantifier
app.dependency_overrides[PredicatesService.get_recommender] = PredicatesRecommenderMock.get_recommender
client = TestClient(app)


def test_recommends_predicates():
    response = client.post('/clustering/predicates', json={'title': 'title', 'abstract': 'abstract'})
    assert response.status_code == 200
    assert 'payload' in response.json()
    assert 'predicates' in response.json()['payload']

    for predicate in response.json()['payload']['predicates']:
        assert 'id' in predicate
        assert 'label' in predicate


def test_semantifies_bioassay():
    response = client.post('/clustering/bioassays', json={'text': 'long text'})
    assert response.status_code == 200
    assert 'payload' in response.json()
    assert 'labels' in response.json()['payload']

    for label in response.json()['payload']['labels']:
        assert 'property' in label
        assert 'resources' in label
