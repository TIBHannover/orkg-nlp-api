# -*- coding: utf-8 -*-
import json
import os

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_extract_table():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    file = open(os.path.join(current_dir, "files", "table.pdf"), "rb")

    payload = {"page_number": 1, "region": [51, 48.75, 168.75, 534.75], "lattice": False}

    response = client.post(
        "/tools/pdf/table/extract",
        files={"file": ("table.pdf", file)},
        data={"payload": json.dumps(payload)},
    )

    file.close()

    assert response.status_code == 200
    assert "payload" in response.json()
    assert "table" in response.json()["payload"]
    assert isinstance(response.json()["payload"]["table"], dict)

    for key in response.json()["payload"]["table"]:
        assert isinstance(response.json()["payload"]["table"][key], list)


def test_convert_pdf():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    file = open(os.path.join(current_dir, "files", "table.pdf"), "rb")

    response = client.post("/tools/pdf/convert", files={"file": ("table.pdf", file)})

    file.close()

    assert response.status_code == 200
    assert "<!DOCTYPE html>" in response.text


def test_scikgtex_extraction():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    file = open(os.path.join(current_dir, "files", "scikgtex.pdf"), "rb")

    response = client.post("/tools/pdf/ski-kg-tex/extract", files={"file": ("scikgtex.pdf", file)})

    file.close()

    assert response.status_code == 200
    assert "payload" in response.json()
    assert "paper" in response.json()["payload"]
    assert isinstance(response.json()["payload"]["paper"], dict)

    # The paper has 4 authors
    assert isinstance(response.json()["payload"]["paper"]["authors"], list)
    assert len(response.json()["payload"]["paper"]["authors"]) == 4

    # The paper has 1 contribution and the first one has 5 values
    assert isinstance(response.json()["payload"]["paper"]["contributions"], list)
    assert len(response.json()["payload"]["paper"]["contributions"]) == 1
    assert len(response.json()["payload"]["paper"]["contributions"][0]["values"]) == 5


def test_scikgtex_extraction_should_fail():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    file = open(os.path.join(current_dir, "files", "table.pdf"), "rb")

    response = client.post("/tools/pdf/ski-kg-tex/extract", files={"file": ("table.pdf", file)})

    file.close()

    assert response.status_code == 500
