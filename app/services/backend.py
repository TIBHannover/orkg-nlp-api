# -*- coding: utf-8 -*-
import os
import urllib.parse as parser
from typing import Optional

import requests

from app.services import OrkgNlpApiService

DEFAULT_PROPERTIES = {
    "researchproblem": "P32",
    "result": "P1",
    "conclusion": "P7072",
    "objective": "P7077",
    "method": "P2",
}
DEFAULT_RESEARCH_FIELD = "ResearchField"


# FIXME: This should use the orkg package and not requests directly
# Relies on https://gitlab.com/TIBHannover/orkg/nlp/orkg-nlp-pypi/-/issues/22
class OrkgBackendService(OrkgNlpApiService):
    _classes_host: str = None
    _predicates_host: str = None

    def __init__(self):
        host: str = os.getenv(
            "ORKG_BACKEND_HOST",
            "http://localhost",
        )
        self._classes_host = parser.urljoin(host, "/api/classes")
        self._predicates_host = parser.urljoin(host, "/api/predicates")

    def lookup_orkg_research_field(self, research_field) -> str:
        host = self._classes_host + "/ResearchField/resources/?"
        host += parser.urlencode({"q": research_field, "exact": True})
        response = requests.request("GET", host).json()
        if response and len(response["content"]) > 0:
            return response["content"][0]["id"]
        else:
            return DEFAULT_RESEARCH_FIELD

    def lookup_orkg_predicate(self, predicate_lbl) -> Optional[str]:
        if predicate_lbl in DEFAULT_PROPERTIES:
            return DEFAULT_PROPERTIES[predicate_lbl]
        host = self._predicates_host + "/?"
        host += parser.urlencode({"q": predicate_lbl, "exact": True})
        response = requests.request("GET", host).json()
        if response and len(response["content"]) > 0:
            return response["content"][0]["id"]
        else:
            return None
