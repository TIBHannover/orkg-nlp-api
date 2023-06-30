# -*- coding: utf-8 -*-
from orkgnlp.annotation import AgriNer, CSNer, ResearchFieldClassifier

from app.common.services.wrapper import ResponseWrapper
from app.services import OrkgNlpApiService


class ResearchFieldClassifierService(OrkgNlpApiService):
    _annotator: ResearchFieldClassifier = None

    def __init__(self, annotator: ResearchFieldClassifier):
        self.annotator = annotator

    def annotate(self, raw_input=None, top_n=None):
        return ResponseWrapper.wrap_json(
            {"annotations": self.annotator(raw_input=raw_input, top_n=top_n)}
        )

    @classmethod
    def get_annotator(cls):
        if not cls._annotator:
            cls._annotator = ResearchFieldClassifier()

        return cls._annotator


class CSNerService(OrkgNlpApiService):
    _annotator: CSNer = None

    def __init__(self, annotator: CSNer):
        self.annotator = annotator

    def annotate(self, title=None, abstract=None):
        annotations = {"title": [], "abstract": []}

        if title and abstract:
            annotations.update(self.annotator(title=title, abstract=abstract))

        elif title:
            annotations["title"] = self.annotator(title=title)

        elif abstract:
            annotations["abstract"] = self.annotator(abstract=abstract)

        return ResponseWrapper.wrap_json({"annotations": annotations})

    @classmethod
    def get_annotator(cls):
        if not cls._annotator:
            cls._annotator = CSNer()

        return cls._annotator


class AgriNerService(OrkgNlpApiService):
    _annotator: AgriNer = None

    def __init__(self, annotator: AgriNer):
        self.annotator = annotator

    def annotate(self, title=None):
        return ResponseWrapper.wrap_json({"annotations": self.annotator(title=title)})

    @classmethod
    def get_annotator(cls):
        if not cls._annotator:
            cls._annotator = AgriNer()

        return cls._annotator
