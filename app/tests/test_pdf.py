import json
import os

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_extract_table():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    file = open(os.path.join(current_dir, 'files', 'table.pdf'), 'rb')

    payload = {
        'page_number': 1,
        'region': [51, 48.75, 168.75, 534.75],
        'lattice': False
    }

    response = client.post(
        '/tools/pdf/table/extract',
        files={'file': ('table.pdf', file)},
        data={
            'payload': json.dumps(payload)
        }
    )

    file.close()

    assert response.status_code == 200
    assert 'table' in response.json()
    assert isinstance(response.json()['table'], dict)

    for key in response.json()['table']:
        assert isinstance(response.json()['table'][key], list)


def test_convert_pdf():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    file = open(os.path.join(current_dir, 'files', 'table.pdf'), 'rb')

    response = client.post(
        '/tools/pdf/convert',
        files={'file': ('table.pdf', file)}
    )

    file.close()

    assert response.status_code == 200
    assert '<!DOCTYPE html>' in response.text
