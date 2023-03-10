# -*- coding: utf-8 -*-
class CSNerMock:
    def __call__(self, title=None, abstract=None):
        annotations = [{"concept": "some_concept", "entities": ["arbitrarily entity"] * 10}] * 10

        if title and abstract:
            return {"title": annotations, "abstract": annotations}

        if title:
            return annotations

        if abstract:
            return annotations

    @staticmethod
    def get_annotator():
        return CSNerMock()


class AgriNerMock:
    def __call__(self, title):
        annotations = [{"concept": "some_concept", "entities": ["arbitrarily entity"] * 10}] * 10

        return annotations

    @staticmethod
    def get_annotator():
        return AgriNerMock()
