# -*- coding: utf-8 -*-
from fastapi.testclient import TestClient

from app.db.connection import get_db
from app.main import app
from tests.db.connection import override_get_db

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_creates_feedback_ok():
    feedback = {
        "service_name": "CS_NER",
        "request": {"hello": "world"},
        "response": {"hello": "world"},
    }
    response = client.post("/feedback/", json={"feedback": feedback})

    assert response.status_code == 200
    assert "payload" in response.json()
    assert "id" in response.json()["payload"]
    assert isinstance(response.json()["payload"]["id"], str)


def test_creates_feedback_fails_service_name_unknown():
    feedback = {
        "service_name": "unknown",
        "request": {"hello": "world"},
        "response": {"hello": "world"},
    }
    response = client.post("/feedback/", json={"feedback": feedback})

    assert response.status_code == 400


def test_creates_feedback_fails_request_empty():
    feedback = {"service_name": "CS_NER", "request": {}, "response": {"hello": "world"}}
    response = client.post("/feedback/", json={"feedback": feedback})

    assert response.status_code == 500


def test_creates_feedback_fails_response_empty():
    feedback = {"service_name": "CS_NER", "request": {"hello": "world"}, "response": {}}
    response = client.post("/feedback/", json={"feedback": feedback})

    assert response.status_code == 500


def test_reads_all_feedbacks_ok():
    response = client.get("/feedback/", params={"skip": 0, "limit": 100})

    assert response.status_code == 200
    assert "payload" in response.json()
    assert "feedbacks" in response.json()["payload"]
    assert isinstance(response.json()["payload"]["feedbacks"], list)

    for feedback in response.json()["payload"]["feedbacks"]:
        assert "id" in feedback
        assert "service_name" in feedback
        assert "request" in feedback
        assert "response" in feedback
