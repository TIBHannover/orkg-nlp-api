from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_recommends_predicates():
    response = client.get('/clustering/predicates', params={'title': 'title', 'abstract': 'abstract'})
    assert response.status_code == 200
    assert 'predicates' in response.json()

    for predicate in response.json()['predicates']:
        assert 'id' in predicate
        assert 'label' in predicate


def test_semantifies_bioassay():
    response = client.get('/clustering/bioassays', params={'text': 'long text'})
    assert response.status_code == 200
    assert 'labels' in response.json()

    for label in response.json()['labels']:
        assert 'property' in label
        assert 'resources' in label
