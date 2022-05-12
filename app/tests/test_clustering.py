from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_recommends_predicates():
    response = client.get('/clustering/predicates', params={'title': 'title', 'abstract': 'abstract'})
    assert response.status_code == 200
