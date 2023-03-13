# -*- coding: utf-8 -*-
from starlette.testclient import TestClient

from app.main import app
from app.services.nli import TemplatesService
from tests.mock.mock_nli import TemplatesRecommenderMock

app.dependency_overrides[
    TemplatesService.get_recommender
] = TemplatesRecommenderMock.get_recommender
client = TestClient(app)


def test_recommends_templates():
    response = client.post("/nli/templates", json={"title": "title", "abstract": "abstract"})
    assert response.status_code == 200
    assert "payload" in response.json()
    assert "templates" in response.json()["payload"]

    for template in response.json()["payload"]["templates"]:
        assert "id" in template
        assert "label" in template
