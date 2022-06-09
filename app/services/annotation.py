from orkgnlp.annotation import CSNer

from app.common.services.wrapper import ResponseWrapper
from app.services import OrkgNlpApiService


class CSNerService(OrkgNlpApiService):

    def __init__(self):
        self.annotator = CSNer()

    def annotate(self, title=None, abstract=None):
        annotations = {'title': [], 'abstract': []}

        if title and abstract:
            annotations.update(self.annotator(title=title, abstract=abstract))

        elif title:
            annotations['title'] = self.annotator(title=title)

        elif abstract:
            annotations['abstract'] = self.annotator(abstract=abstract)

        return ResponseWrapper.wrap_json({'annotations': annotations})
