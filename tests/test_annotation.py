from fastapi.testclient import TestClient

from app.main import app
from app.services.annotation import CSNerService
from tests.mock.mock_annotation import CSNerMock

app.dependency_overrides[CSNerService.get_annotator] = CSNerMock.get_annotator
client = TestClient(app)

title = 'Open Research Knowledge Graph: Next Generation Infrastructure for Semantic Scholarly Knowledge'
abstract = 'Despite improved digital access to scholarly knowledge in recent decades, scholarly communication remains exclusively document-based. In this form, scholarly knowledge is hard to process automatically. We present the first steps towards a knowledge graph based infrastructure that acquires scholarly knowledge in machine actionable form thus enabling new possibilities for scholarly knowledge curation, publication and processing. The primary contribution is to present, evaluate and discuss multi-modal scholarly knowledge acquisition, combining crowdsourced and automated techniques. We present the results of the first user evaluation of the infrastructure with the participants of a recent international conference. Results suggest that users were intrigued by the novelty of the proposed infrastructure and by the possibilities for innovative scholarly knowledge processing it could enable.'


def test_annotates_paper_full():
    response = client.post('/annotation/csner', json={'title': title, 'abstract': abstract})

    assert response.status_code == 200
    assert 'payload' in response.json()
    assert 'annotations' in response.json()['payload']
    assert 'title' in response.json()['payload']['annotations']
    assert 'abstract' in response.json()['payload']['annotations']

    for key in response.json()['payload']['annotations']:
        assert_annotations_list(response.json()['payload']['annotations'][key])


def test_annotates_paper_title():
    response = client.post('/annotation/csner', json={'title': title})

    assert response.status_code == 200
    assert 'payload' in response.json()
    assert 'annotations' in response.json()['payload']
    assert 'title' in response.json()['payload']['annotations']
    assert 'abstract' in response.json()['payload']['annotations']

    assert_annotations_list(response.json()['payload']['annotations']['title'])
    assert len(response.json()['payload']['annotations']['abstract']) == 0


def test_annotates_paper_abstract():
    response = client.post('/annotation/csner', json={'abstract': abstract})

    assert response.status_code == 200
    assert 'payload' in response.json()
    assert 'annotations' in response.json()['payload']
    assert 'title' in response.json()['payload']['annotations']
    assert 'abstract' in response.json()['payload']['annotations']

    assert len(response.json()['payload']['annotations']['title']) == 0
    assert_annotations_list(response.json()['payload']['annotations']['abstract'])


def assert_annotations_list(annotations):
    assert isinstance(annotations, list)
    assert len(annotations) > 0

    for annotation in annotations:
        assert 'concept' in annotation
        assert 'entities' in annotation
