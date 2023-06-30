# -*- coding: utf-8 -*-
from fastapi.testclient import TestClient

from app.main import app
from app.services.annotation import (
    AgriNerService,
    CSNerService,
    ResearchFieldClassifierService,
)
from tests.mock.mock_annotation import (
    AgriNerMock,
    CSNerMock,
    ResearchFieldClassifierMock,
)

app.dependency_overrides[CSNerService.get_annotator] = CSNerMock.get_annotator
app.dependency_overrides[AgriNerService.get_annotator] = AgriNerMock.get_annotator
app.dependency_overrides[
    ResearchFieldClassifierService.get_annotator
] = ResearchFieldClassifierMock.get_annotator
client = TestClient(app)

title = "Open Research Knowledge Graph: Next Generation Infrastructure for Semantic Scholarly Knowledge"
abstract = (
    "Despite improved digital access to scholarly knowledge in recent decades, scholarly communication "
    "remains exclusively document-based. In this form, scholarly knowledge is hard to process automatically. "
    "We present the first steps towards a knowledge graph based infrastructure that acquires scholarly knowledge in "
    "machine actionable form thus enabling new possibilities for scholarly knowledge curation, publication and "
    "processing. The primary contribution is to present, evaluate and discuss multi-modal scholarly knowledge "
    "acquisition, combining crowdsourced and automated techniques. We present the results of the first user "
    "evaluation of the infrastructure with the participants of a recent international conference. Results suggest "
    "that users were intrigued by the novelty of the proposed infrastructure and by the possibilities for innovative "
    "scholarly knowledge processing it could enable."
)


def test_annotates_rfclf_full():
    top_n = 10
    response = client.post(
        "/annotation/rfclf", json={"raw_input": title + "   " + abstract, "top_n": top_n}
    )

    assert response.status_code == 200
    assert "payload" in response.json()
    assert "annotations" in response.json()["payload"]
    assert len(response.json()["payload"]["annotations"]) == top_n


def test_annotates_cs_paper_full():
    response = client.post("/annotation/csner", json={"title": title, "abstract": abstract})

    assert response.status_code == 200
    assert "payload" in response.json()
    assert "annotations" in response.json()["payload"]
    assert "title" in response.json()["payload"]["annotations"]
    assert "abstract" in response.json()["payload"]["annotations"]

    for key in response.json()["payload"]["annotations"]:
        assert_annotations_list(response.json()["payload"]["annotations"][key])


def test_annotates_cs_paper_title():
    response = client.post("/annotation/csner", json={"title": title})

    assert response.status_code == 200
    assert "payload" in response.json()
    assert "annotations" in response.json()["payload"]
    assert "title" in response.json()["payload"]["annotations"]
    assert "abstract" in response.json()["payload"]["annotations"]

    assert_annotations_list(response.json()["payload"]["annotations"]["title"])
    assert len(response.json()["payload"]["annotations"]["abstract"]) == 0


def test_annotates_cs_paper_abstract():
    response = client.post("/annotation/csner", json={"abstract": abstract})

    assert response.status_code == 200
    assert "payload" in response.json()
    assert "annotations" in response.json()["payload"]
    assert "title" in response.json()["payload"]["annotations"]
    assert "abstract" in response.json()["payload"]["annotations"]

    assert len(response.json()["payload"]["annotations"]["title"]) == 0
    assert_annotations_list(response.json()["payload"]["annotations"]["abstract"])


def test_annotates_agri_paper():
    response = client.post("/annotation/agriner", json={"title": title})

    assert response.status_code == 200
    assert "payload" in response.json()
    assert "annotations" in response.json()["payload"]

    assert_annotations_list(response.json()["payload"]["annotations"])


def assert_annotations_list(annotations):
    assert isinstance(annotations, list)
    assert len(annotations) > 0

    for annotation in annotations:
        assert "concept" in annotation
        assert "entities" in annotation
